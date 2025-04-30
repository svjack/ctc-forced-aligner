### pip install pydub datasets

#!/usr/bin/env python
# coding: utf-8

# In[ ]:


ctc-forced-aligner --audio_path "ganyu_audio/0_audio.wav" --text_path "ganyu_audio/0_audio.txt" --language "zh" --romanize


# In[32]:


import pandas as pd
pd.read_json("ganyu_audio/0_audio.json")["segments"].iloc[0]



# In[ ]:


ctc-forced-aligner --audio_path "ganyu_audio/0_audio.wav" --text_path "sub0.txt" --language "zh" --romanize


# In[4]:


import pandas as pd
pd.read_json("ganyu_audio/0_audio.json")["segments"].iloc[0]


# In[6]:


from pydub import AudioSegment

def slice_audio(input_path, start_sec, end_sec, output_path):
    """
    切割音频片段并保存到指定路径
    
    参数:
        input_path (str): 输入音频文件路径（如 'input.mp3'）
        start_sec (float): 开始时间（秒）
        end_sec (float): 结束时间（秒）
        output_path (str): 输出文件路径（如 'output.wav'）
    """
    # 加载音频文件
    audio = AudioSegment.from_file(input_path)
    
    # 转换为毫秒（pydub 使用毫秒为单位）
    start_ms = start_sec * 1000
    end_ms = end_sec * 1000
    
    # 切割音频
    sliced_audio = audio[start_ms:end_ms]
    
    # 保存到输出路径（自动根据文件后缀确定格式）
    sliced_audio.export(output_path, format=output_path.split('.')[-1])
    print(f"音频已切割并保存到: {output_path}")

# 示例用法
slice_audio("ganyu_audio/0_audio.wav", 1.533, 2.352, "output.wav")


# In[8]:


df = pd.read_csv("genshin_impact_ganyu_audio_sample/metadata.csv")
df


# In[26]:


#print(df.head(3).to_markdown())
import re
def split_chinese_text(text):
    # 正则说明：
    # - [\u4e00-\u9fff]：匹配基本中文字符
    # - [\u3000-\u303F]：匹配中文标点符号（如？、。！）
    # - [\uFF00-\uFFEF]：匹配全角符号（如“”「」）
    # - + 表示匹配1个或多个连续字符
    pattern = re.compile(r'([\u4e00-\u9fff]+)')
    matches = pattern.findall(text)
    # 过滤空匹配项并返回
    return [match for match in matches if match.strip()]

import re

def split_chinese_text(text):
    # 正则说明：
    # - [\u4e00-\u9fff]：匹配基本中文字符
    # - [\u3000-\u303F]：匹配中文标点符号（如？、。！）
    # - [\uFF00-\uFFEF]：匹配全角符号（如“”「」）
    # - + 表示匹配1个或多个连续字符
    pattern = re.compile(r'([\u4e00-\u9fff]+)')
    matches = pattern.findall(text)
    # 过滤空匹配项并将每个匹配项添加到原始文本的尾部
    result = []
    for match in matches:
        if match.strip():
            result.append(text + match)  # 将原始文本和匹配的中文字符串拼接
    return result

import re

def split_chinese_text(text):
    # 匹配中文字符（包括中文标点符号）
    pattern = re.compile(r'([\u4e00-\u9fff\u3000-\u303F\uFF00-\uFFEF]+)')
    
    # 使用 re.split() 进行分割，但保留分隔符
    parts = re.split(pattern, text)
    
    # 过滤空字符串并返回非空部分
    return [part for part in parts if part.strip()]

import re

def split_by_punctuation(text):
    # 匹配标点符号（中文 + 英文标点）
    pattern = re.compile(r'([\u3000-\u303F\uFF00-\uFFEF!"，。#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~])')
    
    # 使用 re.split() 分割，但保留标点
    parts = re.split(pattern, text)
    
    # 过滤空字符串并返回
    return [part for part in parts if part.strip()]

import re
def split_chinese_text(text):
    # 正则说明：
    # - [\u4e00-\u9fff]：匹配基本中文字符
    # - [\u3000-\u303F]：匹配中文标点符号（如？、。！）
    # - [\uFF00-\uFFEF]：匹配全角符号（如“”「」）
    # - + 表示匹配1个或多个连续字符
    pattern = re.compile(r'([\u4e00-\u9fff]+)')
    matches = pattern.findall(text)
    # 过滤空匹配项并返回
    return [match for match in matches if match.strip()]
    


# In[27]:


df["prompt"].map(split_chinese_text)


# In[20]:


text = "Hello你好World世界！Python编程"
print(split_chinese_text(text))


# In[ ]:





# In[23]:


text = "你好，世界！Hello, world? 这是测试。"
print(split_by_punctuation(text))


# In[31]:


import re
def split_chinese_text(text):
    # 正则说明：
    # - [\u4e00-\u9fff]：匹配基本中文字符
    # - [\u3000-\u303F]：匹配中文标点符号（如？、。！）
    # - [\uFF00-\uFFEF]：匹配全角符号（如“”「」）
    # - + 表示匹配1个或多个连续字符
    pattern = re.compile(r'([\u4e00-\u9fff]+)')
    matches = pattern.findall(text)
    # 过滤空匹配项并返回
    return [match for match in matches if match.strip()]

df = pd.read_csv("genshin_impact_ganyu_audio_sample/metadata.csv")
df

df["prompt_l"] = df["prompt"].map(split_chinese_text)
df = df.explode("prompt_l").dropna().drop_duplicates()[["file_name", "prompt_l"]]
print(df.head(3).to_markdown())


# In[ ]:


ctc-forced-aligner --audio_path "ganyu_audio/0_audio.wav" --text_path "ganyu_audio/0_audio.txt" --language "zh" --romanize --split_size "sentence"

