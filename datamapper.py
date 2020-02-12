import os, csv, yaml

from config import SOURCE_DIR

header = ['lin_x','ang_z','file_path']
directory = SOURCE_DIR


subdirectories = [x for x in os.walk(directory)]

# set csv and write header. this a file generated
# in the same folder you started datamapper.py from
with open('mapped.csv', 'wt') as f:
    csv_writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    csv_writer.writerow(header)

    # find yamls down the tree
    for subdir in subdirectories:
        for filename in os.listdir(subdir[0]):
            if filename.endswith(".yaml"):

                    stream = open(subdir[0] + "/" + filename, 'r')
                    prof = yaml.load(stream)

                    for data in prof:
                        # print(data)

                        #singular yaml processing

                        datapoints = data.get("action_messages").get("/nr/engine/input/actions")

                        lin_x = datapoints.get("linear").get("x")
                        ang_z = datapoints.get("angular").get("z")


                        file_path = subdir[0] + data.get("camera_messages")[0]

                        print(file_path)
                        row = [lin_x, ang_z,file_path]

                        csv_writer.writerow(row)
            else:
                continue

