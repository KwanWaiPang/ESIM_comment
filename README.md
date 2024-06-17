[comment]: <> (# DEVO)

<!-- PROJECT LOGO -->

<p align="center">

  <h1 align="center"> ESIM及VID2E (个人使用版本)
  </h1>

[comment]: <> (  <h2 align="center">PAPER</h2>)
  <h3 align="center">
  <a href="https://github.com/KwanWaiPang/DEVO_comment">DEVO Github</a> 
  | <a href="https://github.com/uzh-rpg/rpg_vid2e">Original Github Page</a>
  </h3>
  <div align="center"></div>

<br>

# 配置记录
* 下载[FILM](https://github.com/google-research/frame-interpolation)
~~~
<!-- 下载到当前目录 -->
wget https://rpg.ifi.uzh.ch/data/VID2E/pretrained_models.zip

<!-- 解压 -->
unzip pretrained_models.zip
~~~

* 创建环境
~~~
conda create --name vid2e python=3.9
conda activate vid2e
pip install -r requirements.txt
conda install -y -c conda-forge pybind11 matplotlib
<!-- 注意要指定一下pytorch的版本 -->
conda install pytorch==1.12.0 torchvision==0.13.0 torchaudio==0.12.0 cudatoolkit=11.3 -c pytorch

~~~

* 安装ESIM
~~~
pip install esim_py/

pip install setuptools==69.5.1
pip install esim_torch/
~~~

## 以TartanAir为例
* [esim_py的使用](https://github.com/uzh-rpg/rpg_vid2e/blob/master/esim_py/README.md)
* [esim_torch的使用](https://github.com/uzh-rpg/rpg_vid2e/blob/master/esim_torch/README.md)

~~~
<!-- 测试esim_py是否安装成功 -->
python esim_py/tests/test.py

python esim_torch/test/test.py
~~~