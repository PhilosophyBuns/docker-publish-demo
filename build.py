# encoding: utf-8
# python : 2.x
import os, tarfile
import urllib2
import sys
import subprocess


# 参考 https://docs.docker.com/engine/api/v1.27/

# 开发：10.20.19.170
# author luoxiao22525
if __name__ == '__main__':
  ## 这里定义使用到的变量

  # tar包文件名
  tarFileName = "vue-demo.tar.gz"
  # docker镜像tag
  tagName = "www.luoxiao.com/vue-demo"
  # docker镜像地址
  dockerHost = "123.56.224.41:2375"
  # dockerHost = "10.128.4.107:2375"

  # dockerHost = "docker.gf.com.cn"
  # docker仓库地址
  dockerRegistry = "www.luoxiao.com"
  #前端重新打包
  execPackage = True
  #push到仓库
  dockerPushImage = False

  #  1.执行npm run build
  if (execPackage) :
    print "-------------------- webpack 打包开始 --------------------"
    popen = subprocess.Popen('npm run build',shell=True,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE,
                             bufsize=1)
    while popen.poll() is None:         # None表示正在执行中
      r = popen.stdout.readline().decode('utf-8')
      sys.stdout.write(r)
    if popen.poll() != 0:                # 不为0表示执行错误
      err = popen.stderr.read().decode('utf-8')
      sys.stdout.write(err)
      sys.exit()
    popen.stdout.close()
    print "-------------------- webpack 打包结束 --------------------"
  print "-------------------- build   操作开始 --------------------"
  # 2.打包dockerfile,nginx.conf,dist
  with tarfile.open(sys.path[0] + "/docker/" + tarFileName, "w:gz") as tar:
    tar.add(sys.path[0] + "/dist", arcname=os.path.basename(sys.path[0] + "/dist"))
    tar.add(sys.path[0] + "/docker/nginx.conf", arcname=os.path.basename(sys.path[0] + "/nginx.conf"))
    tar.add(sys.path[0] + "/docker/Dockerfile", arcname=os.path.basename(sys.path[0] + "/Dockerfile"))
  ## 3读取打包的文件流
  with open(sys.path[0] + "/docker/" + tarFileName, mode='rb') as f:
    fileData = f.read()
  # if(os.path.exists(sys.path[0] + "/docker/" + tarFileName)):
    # os.remove(sys.path[0] + "/docker/" + tarFileName)
  ## 4.发送打包请求
  request = urllib2.Request(("http://"+dockerHost + "/build?t=%s") % tagName)
  request.add_header('content-TYPE', 'application/x-tar')
  response = urllib2.urlopen(request, data=fileData)
  print response.read()
  print "-------------------- build   操作结束 --------------------"


  ## 5.发送push请求
  if (dockerPushImage) :
    print "-------------------- push    操作开始 --------------------"
    pushRequest = urllib2.Request(("http://" + dockerHost + "/images/%s/push") % tagName)
    pushRequest.add_header('content-type','application/json')
    pushRequest.add_header('x-registry-auth','null')
    data = ''
    pushResponse = urllib2.urlopen(pushRequest,data = data)
    print pushResponse.read()
    print "-------------------- push    操作结束 --------------------"


