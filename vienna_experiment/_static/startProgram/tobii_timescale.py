import math , pywt , numpy as np
import tobii_research as tr
import psycopg2
import time

import sys
import math
import datetime
import threading

from scipy.signal import savgol_filter

################################

# Define a global variable for running state
running = False
serverIP = None
eyeTracker = None
license_file = None
global mappingID 

global conn
global cursor






#Just needed for testing
def generate_realistic_raw_data(length, frequency=0.1, amplitude=4.0, noise_std=0.5):
    """
    Generates realistic raw pupil diameter data.

    Parameters:
        length (int): Length of the data.
        frequency (float): Frequency of the sinusoidal waveform.
        amplitude (float): Amplitude of the sinusoidal waveform.
        noise_std (float): Standard deviation of the Gaussian noise.

    Returns:
        np.ndarray: Generated raw pupil diameter data.
    """
    time = np.linspace(0, 1, length)
    clean_signal = amplitude * np.sin(2 * np.pi * frequency * time)
    noise = np.random.normal(0, noise_std, length)
    raw_data = clean_signal + noise
    return raw_data


def calculate_normalized_ripa(raw_data, buffer_length=250, m_sg=6, n_sg=10, threshold_factor=0.165):
    """
    Calculates the normalized RIPA (Real-time Index of Pupillometric Activity).

    Parameters:
        raw_data (np.ndarray): Raw pupil diameter data.
        buffer_length (int): Length of the buffer.
        m_sg (int): Savitzky-Golay filter half-width.
        n_sg (int): Savitzky-Golay polynomial order.
        threshold_factor (float): Threshold factor for the RIPA calculation.

    Returns:
        float: Calculated normalized RIPA.
    """
    # Compute low-pass filtered data
    x_lowpass = savgol_filter(raw_data, window_length=m_sg * 2 + 1, polyorder=n_sg)

    # Compute high-pass filtered data
    x_highpass = raw_data - x_lowpass

    # Compute low-to-high-frequency ratio
    x_ratio = x_lowpass / x_highpass

    # Compute modulus maxima
    m = np.zeros_like(x_ratio)
    for t in range(1, buffer_length - 1):
        if abs(x_ratio[t]) > abs(x_ratio[t - 1]) and abs(x_ratio[t]) > abs(x_ratio[t + 1]):
            m[t] = np.sign(x_ratio[t]) * abs(x_ratio[t])

    # Calculate threshold
    threshold = threshold_factor * np.std(m)

    # Compute RIPA
    ripa_count = np.sum(np.abs(x_ratio) > m + threshold)

    # Normalize RIPA
    normalized_ripa = 1 - ripa_count / buffer_length

    return normalized_ripa


# Generate example realistic raw data
raw_data = generate_realistic_raw_data(250)

# Calculate normalized RIPA
normalized_ripa = calculate_normalized_ripa(raw_data)
print("Normalized RIPA:", normalized_ripa)



def establishConnection(serverIP):
    connection = f"postgres://postgres:password@{serverIP}:5432/riro2023"
    global conn
    global cursor
    #connect to Timescale database using the psycopg2 connect function
    conn = psycopg2.connect(connection)
    cursor = conn.cursor()
    
    #create a table for eye tracker data if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eyedata40 (
            id serial PRIMARY KEY,
            eyetracker_id TEXT,
            mappingID TEXT,
            time_stamp TIMESTAMP(3),
            first_pupil_left DOUBLE PRECISION,
            first_pupil_right DOUBLE PRECISION,
            gaze_x DOUBLE PRECISION,
            gaze_y DOUBLE PRECISION,
            system_time_stamp DOUBLE PRECISION,
            left_gaze_point_validity DOUBLE PRECISION,
            right_gaze_point_validity DOUBLE PRECISION,
            gaze_left_x DOUBLE PRECISION,
            gaze_left_y DOUBLE PRECISION,
            gaze_right_x DOUBLE PRECISION,
            gaze_right_y DOUBLE PRECISION,
            left_pupil_validity DOUBLE PRECISION,
            right_pupil_validity DOUBLE PRECISION,
            left_pupil_diameter DOUBLE PRECISION,
            right_pupil_diameter DOUBLE PRECISION,
            ipa_left DOUBLE PRECISION,
            ipa_right DOUBLE PRECISION
        );
    """)
    
    conn.commit() #save the changes

 
def initializeTracker():

    # Find Eye Tracker and Apply License (edit to suit actual tracker serial no)
    ft = tr.find_all_eyetrackers()
    global eyeTracker
    if len(ft) == 0:
        print("No Eye Trackers found!?")
        return False

    else:
        # Pick first tracker
        
        eyeTracker = ft[0]
        print("Found Tobii Tracker at '%s'" % (eyeTracker.address))
        return True


def checkLicense(license_file):
    # Apply license
    if license_file != "":
        with open(license_file, "rb") as f:
            license = f.read()

            res = eyeTracker.apply_licenses(license)
            if len(res) == 0:
                print("Successfully applied license from single key")
            else:
                print("Failed to apply license from single key. Validation result: %s." % (res[0].validation_result))
                
    else:
        print("No license file installed")


gaze_data_structure = [
    ('system_time_stamp', 1), 

    ('left_gaze_point_validity',  1),
    ('right_gaze_point_validity',  1),

    ('left_gaze_point_on_display_area',  2),
    ('right_gaze_point_on_display_area',  2),

    ('left_pupil_validity', 1),
    ('right_pupil_validity', 1),

    ('left_pupil_diameter',  1),
    ('right_pupil_diameter',  1)
]

def get_current_time_microseconds():
    current_time_with_microseconds = datetime.datetime.now()
    return current_time_with_microseconds

def calculate_gaze(left_gaze_point_on_display_area, right_gaze_point_on_display_area):
    xs = (left_gaze_point_on_display_area[0], right_gaze_point_on_display_area[0])
    ys = (left_gaze_point_on_display_area[1], right_gaze_point_on_display_area[1])   
    if all([x != -1.0 for x in xs]) and all([y != -1.0 for y in ys]):
        # take x and y averages
        avgGazePos = np.nanmean(xs), np.nanmean(ys)
    else:
        # or if no data, hide points by showing off screen
        avgGazePos = (np.nan, np.nan)
    print(avgGazePos)
    return avgGazePos

def unpack_gaze_data(gaze_data,firstPupilLeft, firstPupilRight):
    gaze_avg = calculate_gaze(gaze_data["left_gaze_point_on_display_area"], firstPupilLeft, firstPupilRight, gaze_data["right_gaze_point_on_display_area"])
    x = [eyeTracker.serial_number, mappingID, get_current_time_microseconds(), gaze_avg[0], gaze_avg[1]]
    for s in gaze_data_structure:
        d = gaze_data[s[0]]
        if isinstance(d, tuple):
            x = x + list(d)
        else:
            x.append(d)
    return tuple(x)




def modmax(d):
    # compute signal modulus
    m = [0.0]*len(d)
    for i in range(len(d)):
        m[i] = math.fabs(d[i])
    # if value is larger than both neighbours , and strictly
    # larger than either , then it is a local maximum
    t = [0.0]*len(d)
    for i in range(len(d)):
        ll = m[i -1] if i >= 1 else m[i]
        oo = m[i]
        rr = m[i+1] if i < len(d)-2 else m[i]
        if (ll <= oo and oo >= rr) and (ll < oo or oo > rr):
        # compute magnitude
            t[i] = math.sqrt(d[i]**2)
        else:
            t[i] = 0.0
    return t


def ipa(dilation_data):
    d = []
    timestamp = []

    for entry in dilation_data:
        d.append(entry[0])
        timestamp.append(entry[1])

    # obtain 2-level DWT of pupil diameter signal d
    try:
        (cA2 ,cD2 ,cD1) = pywt.wavedec(d,'sym16','per',level =2)
    except ValueError :
        return
    # get signal duration (in seconds)
    tt = (int(timestamp[-1]) -int(timestamp[0])) / 1e+6
    print("TIME:::", tt)
    # normalize by 1/2j , j = 2 for 2-level DWT
    cA2[:] = [x / math.sqrt (4.0) for x in cA2]
    cD1[:] = [x / math.sqrt (2.0) for x in cD1]
    cD2[:] = [x / math.sqrt (4.0) for x in cD2]
    # detect modulus maxima , see Listing 2
    cD2m = modmax(cD2)
    # threshold using universal threshold λuniv = σˆp(2logn)
    # where σˆ is the standard deviation of the noise
    λuniv = np.std(cD2m) * math.sqrt(2.0*np.log2(len(cD2m )))
    cD2t = pywt.threshold(cD2m ,λuniv,mode="hard")
    # compute IPA
    ctr = 0
    for i in range(len(cD2t)):
        if math.fabs(cD2t[i]) > 0: ctr += 1
    IPA = float(ctr)/tt
    return IPA


def append_ripa(lst, value1, value2):
    return [(tup + (value1, value2)) for tup in lst]



def format_gaze_data(input_tuple): 
    input_list = list(input_tuple)
    for i in range(len(input_list)):
        if i > 2:
            input_list[i] = float(input_list[i])
    return tuple(input_list)

def gaze_data_callback(gaze_data):
    '''send gaze data'''

    '''
    This is what we get from the tracker:
    device_time_stamp
    left_gaze_origin_in_trackbox_coordinate_system (3)
    left_gaze_origin_in_user_coordinate_system (3)
    left_gaze_origin_validity
    left_gaze_point_in_user_coordinate_system (3)
    left_gaze_point_on_display_area (2)
    left_gaze_point_validity
    left_pupil_diameter
    left_pupil_validity
    right_gaze_origin_in_trackbox_coordinate_system (3)
    right_gaze_origin_in_user_coordinate_system (3)
    right_gaze_origin_validity
    right_gaze_point_in_user_coordinate_system (3)
    right_gaze_point_on_display_area (2)
    right_gaze_point_validity
    right_pupil_diameter
    right_pupil_validity
    system_time_stamp 
    '''

    try:
        global halted
        global sample
        global dilationLeft
        global dilationRight
        global firstPupil
        global firstPupilLeft
        global firstPupilright
        
        sts = gaze_data['system_time_stamp'] / 1000000.

        if not firstPupil:
            firstPupilLeft = gaze_data["left_pupil_diameter"]
            firstPupilright = gaze_data["left_pupil_diameter"]

        if gaze_data['left_pupil_validity'] == 1 and gaze_data['right_pupil_validity']:
            firstPupil = True

        if len(sample) < 30: 
            sample.append(format_gaze_data(unpack_gaze_data(gaze_data, firstPupilLeft, firstPupilright)))
            dilationLeft.append((gaze_data["left_pupil_diameter"], gaze_data['system_time_stamp']))
            dilationRight.append((gaze_data["right_pupil_diameter"], gaze_data['system_time_stamp']))
        else:
            dilationLeft.append((gaze_data["left_pupil_diameter"], gaze_data['system_time_stamp']))
            dilationRight.append((gaze_data["right_pupil_diameter"], gaze_data['system_time_stamp']))
            sample.append(format_gaze_data(unpack_gaze_data(gaze_data)))
            sample = append_ripa(sample, calculate_normalized_ripa(dilationLeft), calculate_normalized_ripa(dilationRight))
            #print(format_gaze_data(unpack_gaze_data(gaze_data)))

            cursor.executemany("""INSERT INTO eyedata40 (
                        eyetracker_id, 
                        mappingID,
                        time_stamp, 
                        first_pupil_left,
                        first_pupil_right,
                        gaze_x,
                        gaze_y,
                        system_time_stamp, 
                        left_gaze_point_validity, 
                        right_gaze_point_validity, 
                        gaze_left_x, 
                        gaze_left_y, 
                        gaze_right_x, 
                        gaze_right_y, 
                        left_pupil_validity, 
                        right_pupil_validity, 
                        left_pupil_diameter, 
                        right_pupil_diameter,
                        ipa_left,
                        ipa_right) 
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", sample)
            #commit changes to the database
            conn.commit()
            print("LEFT:::", ipa(dilationLeft))
            print("RIGHT:::", ipa(dilationRight))
            sample = []
            dilationLeft = []
            dilationRight = []
    except:
        print("Error in callback: ")
        print(sys.exc_info())

        halted = True

# Define a function that starts the eye tracker and runs until stopped
def start():
    # Subscribe to the gaze data stream
    eyeTracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    # Print a message
    print("Gaze tracking started")
    # Run until stopped
    while running:
        time.sleep(0.1)
    # Unsubscribe from the gaze data stream
    eyeTracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
    # Print a message
    print("Gaze tracking stopped")


def end_gaze_tracking():
    if eyeTracker != None:
        eyeTracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
        #close the connection
        conn.close()
        quit()
    else:
        print("No Tracker")


halted = False
sample = []
dilationLeft = []
dilationRight = []
firstPupil = False
firstPupilLeft = None
firstPupilRight = None

def startTracking(serverIP, filepath, tmp_mappingID):
    license_file = filepath
    global mappingID
    mappingID = tmp_mappingID
    establishConnection(serverIP)
    if initializeTracker():
        checkLicense(license_file)
        print("Tobii Initialized")
        
        global running
        # Set the running state to True
        running = True
        # Create a thread for the start function
        t = threading.Thread(target=start)
        # Start the thread
        t.start()
  
def stopTracking():
    print("terminating tracking now")
    end_gaze_tracking()
    print("Das Programm läuft noch.")
    sys.exit() #beendet die Laufzeit

        