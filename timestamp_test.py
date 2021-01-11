import rosbag
import numpy as np
import pandas as pd

# bag path and read bag info
bag_file = '/home/wzy/data/bagdata/kitti_2011_10_03_drive_0027_synced.bag'
bag = rosbag.Bag(bag_file,"r")
info = bag.get_type_and_topic_info()
print("bag_file: ",bag_file)
print("topic_timestamp_diff")

for topic in info.topics:

    bag_data = bag.read_messages(topic)
    max_diff = 0    # max time diff
    min_diff = 0    # min time diff
    max_c = 0       # max time diff location
    min_c = 0       # min time diff location
    diff_list = []  # store time diff
    diff_sum = 0    # time diff sum
    data_count = 0  # time diff count
    t_last = 0

    # init flag
    t_init_flag = 0
    diff_init_flag = 0

    print("####################")
    print(topic, "  hz:", info.topics[topic].frequency, "  msg_count:", info.topics[topic].message_count, "  msg_type:",
          info.topics[topic].msg_type)


    for data_topic, msg, t in bag_data:
        if t_init_flag == 0:  # init t_last
            t_last = t
            t_init_flag = 1
        else:
            t_diff_temp = t.to_sec() - t_last.to_sec()
            data_count = data_count + 1
            diff_list.insert(data_count,t_diff_temp)
            diff_sum = diff_sum + t_diff_temp
            if diff_init_flag == 0:  # init max_diff
                max_diff = t_diff_temp
                min_diff = t_diff_temp
                diff_init_flag = 1
                t_last = t
            else:
                if t_diff_temp > max_diff:
                    max_diff = t_diff_temp
                    max_c = data_count
                if t_diff_temp < min_diff:
                    min_diff = t_diff_temp
                    min_c = data_count
                t_last = t

    # print info of diff, such as max, min ,average
    print("max_diff: ",max_diff,"s","  location:",max_c)
    print("min_diff: ",min_diff,"s","  location:",min_c)
    if data_count == 0:
        print("average_diff", 0 , "s")
    else:
        print("average_diff",diff_sum/data_count,"s")

    name = []      #change '/' to '_' in topic name
    for i in range(len(topic)):
        if topic[i] == '/':
            name.insert(i, '_')
        else:
            name.insert(i, topic[i])
    file_name = "".join(name)

    txt_path = '/home/wzy/data/bagdata/topic_diff/kitti_2011_10_03_drive_0027_synced/' + file_name + '.txt'
    diff_array = np.array(diff_list)     # save list to numpy.array
    np.savetxt(txt_path, diff_array, delimiter='\n', newline='\r\n')    # save numpy.array to txt to save time diff