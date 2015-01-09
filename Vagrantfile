# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"


$install_dependencies = <<SCRIPT
apt-get update
apt-get -y install screen python3 python3-psutil
apt-get -y build-dep nginx-full
SCRIPT

$install_nginx = <<SCRIPT
wget http://nginx.org/download/nginx-1.7.8.tar.gz
tar -xf nginx-1.7.8.tar.gz
cd nginx-1.7.8/
./configure --prefix=$(pwd)/../nginx
make
make install
SCRIPT

$start_servers = <<SCRIPT
echo "================"
echo "Starting Servers"
echo "================"
cd /web
screen -c /dev/null -dmS server_sessionpersistence1 python3 load.py 4001
screen -c /dev/null -dmS server_sessionpersistence2 python3 load.py 4002
screen -c /dev/null -dmS server_sessionpersistence3 python3 load.py 4003
screen -c /dev/null -dmS server_sessionpersistence4 python3 load.py 4004
SCRIPT

$start_nginx = <<SCRIPT
ps cax | grep nginx > /dev/null
if [ $? -eq 0 ]; then
  echo "================"
  echo "Restarting nginx"
  echo "================"
  killall nginx
else
  echo "=============="
  echo "Starting nginx"
  echo "=============="
fi
nginx/sbin/nginx
SCRIPT


Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "ubuntu/trusty64"

  config.vm.synced_folder "web", "/web"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  config.vm.network "public_network"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine.
  # Session Persistence
  config.vm.network "forwarded_port", guest: 7000, host: 7000
  # Round Robin
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  # Least Connections
  config.vm.network "forwarded_port", guest: 9000, host: 9000
  # Python servers
  config.vm.network "forwarded_port", guest: 4001, host: 4001
  config.vm.network "forwarded_port", guest: 4002, host: 4002
  config.vm.network "forwarded_port", guest: 4003, host: 4003
  config.vm.network "forwarded_port", guest: 4004, host: 4004

  config.vm.provision "shell", inline: $install_dependencies
  config.vm.provision "shell", inline: $install_nginx, privileged: false
  config.vm.provision "file", source: "nginx_load_balancer.conf", destination: "nginx/conf/nginx.conf"
  config.vm.provision "shell", inline: $start_servers, run: "always", privileged: false
  config.vm.provision "shell", inline: $start_nginx, run: "always", privileged: false
end
