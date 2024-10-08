import vertexai
from vertexai.generative_models import GenerativeModel, Content, FunctionDeclaration, Part, Tool
import pandas as pd
import json
import os
import pandas as pd
import numpy as np
import time
from vertexai import init


init(project="green-radius-321616")

model = GenerativeModel("gemini-1.5-pro", generation_config={"response_mime_type": "application/json"})

def modularize(topics, course):
  res = model.generate_content(f"make modules and make chapter names within sequence of the topics: {topics} for the course: {course} with atleast 3-4 topics in a module" + "and follow the JSON Schema example: ' { modules = ['Module 1: ModuleName1', 'Module 1: ModuleName1','Module 1: ModuleName1', 'Module 1: ModuleName1' ,'Module2: ModuleName2, 'Module2: ModuleName2', 'Module2: ModuleName2', 'Module3: ModuleName3'... (entries must be with same no of topics )] , numbers = [1,1,1,1,2,2,2,3...(entries must be with same no of topics)] }'")
  modules = json.loads(res.text)["modules"]
  module_nos = json.loads(res.text)["numbers"]

  return modules, module_nos

def adjust_array(array, df):
    if len(array) < len(df):
        # Extend the array by duplicating the last entry
        extra_rows = len(df) - len(array)
        array = np.concatenate([array, [array[-1]] * extra_rows])
    elif len(array) > len(df):
        # Slice the array to fit the DataFrame
        array = array[:len(df)]
    return array


if __name__ == "__main__":
    directory = r"scraped"
    output = r'modularized'
    failed = r'failed'

    for name in os.listdir(directory):
        for sub_name in os.listdir(os.path.join(directory, name)):

            if os.path.exists(os.path.join(output,name,sub_name)):
                pass

            with open(os.path.join(directory, name, sub_name)) as f:
                df = pd.read_csv(os.path.join(directory, name, sub_name))

                topics = df['TopicName'].to_list()
                course = df['CourseName'].to_list()[0]

                time.sleep(60)

                try:
                    modules, module_nos = modularize(topics, course)
                    df['Module'] = adjust_array(np.array(modules), df)
                    df['ModuleNo'] = adjust_array(np.array(module_nos), df)

                    if not os.path.exists(os.path.join(output, name)):
                        os.makedirs(os.path.join(output, name))

                    df.to_csv(os.path.join(output, name, sub_name), index=False)
                    print(f"saved {os.path.join(directory, name, sub_name)}")

                except:
                    if not os.path.exists(os.path.join(failed, name)):
                        os.makedirs(os.path.join(failed, name))

                    df.to_csv(os.path.join(failed, name, sub_name), index=False)
                    print(f"failed {os.path.join(directory, name, sub_name)}")

                    pass