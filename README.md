[comment]: <> (# DEVO)

<!-- PROJECT LOGO -->

<p align="center">

  <h1 align="center"> ESIM及VID2E (个人使用版本)
  </h1>

[comment]: <> (  <h2 align="center">PAPER</h2>)
  <h3 align="center">
  <a href="https://kwanwaipang.github.io/File/Blogs/Poster/esim.html">Blog</a> 
  | <a href="https://github.com/uzh-rpg/rpg_vid2e">Original Github Page</a>
  </h3>
  <div align="center"></div>

<br>

# 配置记录
* 下载[FILM](https://github.com/google-research/frame-interpolation)，用于视频、图像插值的（upsampled）
~~~
<!-- 下载到当前目录 -->
wget https://rpg.ifi.uzh.ch/data/VID2E/pretrained_models.zip

<!-- 解压 -->
unzip pretrained_models.zip
~~~

* 创建环境
~~~
<!-- 删除已有环境 -->
conda env list
conda remove --name vid2e --all

<!-- 遇到conda创建很慢 -->
conda config --show #看看channels
conda config --show channels
conda config --remove channels conda-forge

conda create --name vid2e python=3.9
conda activate vid2e
pip install -r requirements.txt
conda install pybind11 #此处不要安装matplotlib
<!-- 注意要指定一下pytorch的版本 -->
conda install pytorch==1.12.0 torchvision==0.13.0 torchaudio==0.12.0 cudatoolkit=11.3 -c pytorch

~~~

* 安装ESIM
~~~
pip install esim_py/

pip install setuptools==69.5.1
pip install esim_torch/
~~~

## 测试是否安装成功以及debug
* [esim_py的使用](https://github.com/uzh-rpg/rpg_vid2e/blob/master/esim_py/README.md)
* [esim_torch的使用](https://github.com/uzh-rpg/rpg_vid2e/blob/master/esim_torch/README.md)
* 先测试是否安装成功
~~~
conda activate vid2e

<!-- 测试esim_py是否安装成功 -->
python esim_py/tests/test.py
#如果报错GLIBCXX_3.4.30
ln -sf /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /home/gwp/miniconda3/envs/vid2e/lib/libstdc++.so.6
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtiff.so.5
~~~
* 然后测试esim_torch，（注意服务器端直接用会报错，因为要可视化，因此采用ipynb）
~~~
python esim_torch/test/test.py
采用ipynb,选择kernel为vide的
在服务器终端安装一下pip install ipykernel 会更快
~~~
* 关于错误“cannot import name 'mplDeprecation' from 'matplotlib._api.deprecation”。应该是在requirements就已经指定了pip install matplotlib==3.5.1，但是作者在conda install -y -c conda-forge pybind11 matplotlib又安装了一次。解决方案见下
~~~
pip install -r requirements.txt --force-reinstall
#然后重启ipynb的kernel，在终端安装更快：pip install ipykernel 
~~~

* 采用Adaptive Upsampling来上采样video。输入的数据目录为example/original，输出数据目录为example/upsampled
~~~
device=cpu
# device=cuda:0
python upsampling/upsample.py --input_dir=example/original --output_dir=example/upsampled --device=$device
~~~

## 测试记录
* first test [link](esim_torch/test/test.ipynb)
* 画不同的event represent [link](esim_torch/test/evaluating_event_representation.ipynb)
* 测试upsampling+ESIM [link](upsample_esim.ipynb)

# 用HKU-dataset生成数据集同时与real event data 进行对比
* 读入rosbag并可视化image及其对应的event [link](rosbag_reading/read_rosbag.ipynb)
* 需要安装rosbag相关的依赖~
~~~
pip install --extra-index-url https://rospypi.github.io/simple/ rospy rosbag

pip install rosbag_pandas

pip install cv_bridge

pip install sensor_msgs --extra-index-url https://rospypi.github.io/simple/

pip install geometry_msgs --extra-index-url https://rospypi.github.io/simple
~~~
* 读入rosbag,然后将其中的10张图片生成event,同时与10张图片期间的真实的event进行可视化对比.[Link](rosbag_reading/generate_sim_event.ipynb)
* 在上面的基础上，改为先对10张图片进行上采样（learning model）然后再生成sim event [link](rosbag_reading/upsampled_generate_sim_event.ipynb)



# 用TartanAir生成event 数据集


# 参考资料
* [画图各种representation](https://github.com/LarryDong/event_representation); 
* [TUB开源的一些event_utils](https://github.com/tub-rip/event_utils); 
* [TUB开源的events_viz](https://github.com/tub-rip/events_viz);
* [DEVO](https://github.com/KwanWaiPang/DEVO_comment);
