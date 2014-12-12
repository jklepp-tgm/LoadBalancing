# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"


$install_dependencies = <<SCRIPT
apt-get update
apt-get -y install screen python3
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

$start_servers_sessionpersistence = <<SCRIPT
cd /web
screen -c /dev/null -dmS server_sessionpersistence1 python3 -m load.py 7001
screen -c /dev/null -dmS server_sessionpersistence2 python3 -m load.py 7002
screen -c /dev/null -dmS server_sessionpersistence3 python3 -m load.py 7003
screen -c /dev/null -dmS server_sessionpersistence4 python3 -m load.py 7004
SCRIPT

$start_servers_roundrobin = <<SCRIPT
cd /web
screen -c /dev/null -dmS server_roundrobin1 python3 -m load.py 8001
screen -c /dev/null -dmS server_roundrobin2 python3 -m load.py 8002
screen -c /dev/null -dmS server_roundrobin3 python3 -m load.py 8003
screen -c /dev/null -dmS server_roundrobin4 python3 -m load.py 8004
SCRIPT

$start_servers_leastconnections = <<SCRIPT
cd /web
screen -c /dev/null -dmS server_leastconnections1 python3 -m load.py 9001
screen -c /dev/null -dmS server_leastconnections2 python3 -m load.py 9002
screen -c /dev/null -dmS server_leastconnections3 python3 -m load.py 9003
screen -c /dev/null -dmS server_leastconnections4 python3 -m load.py 9004
SCRIPT

$start_nginx = <<SCRIPT
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
  config.vm.network "forwarded_port", guest: 7001, host: 7001
  config.vm.network "forwarded_port", guest: 7002, host: 7002
  config.vm.network "forwarded_port", guest: 7003, host: 7003
  config.vm.network "forwarded_port", guest: 7004, host: 7004
  # Round Robin
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 8001, host: 8001
  config.vm.network "forwarded_port", guest: 8002, host: 8002
  config.vm.network "forwarded_port", guest: 8003, host: 8003
  config.vm.network "forwarded_port", guest: 8004, host: 8004
  # Least Connections
  config.vm.network "forwarded_port", guest: 9000, host: 9000
  config.vm.network "forwarded_port", guest: 9001, host: 9001
  config.vm.network "forwarded_port", guest: 9002, host: 9002
  config.vm.network "forwarded_port", guest: 9003, host: 9003
  config.vm.network "forwarded_port", guest: 9004, host: 9004

  config.vm.provision "shell", inline: $install_dependencies
  config.vm.provision "shell", inline: $install_nginx, privileged: false
  config.vm.provision "file", source: "nginx_load_balancer.conf", destination: "nginx/conf/nginx.conf"
  config.vm.provision "shell", inline: $start_servers_sessionpersistence, run: "always", privileged: false
  config.vm.provision "shell", inline: $start_servers_roundrobin, run: "always", privileged: false
  config.vm.provision "shell", inline: $start_servers_leastconnections, run: "always", privileged: false
  config.vm.provision "shell", inline: $start_nginx, run: "always", privileged: false
end
