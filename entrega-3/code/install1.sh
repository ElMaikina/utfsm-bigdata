#!/bin/bash

# === CONFIGURACIÓN ===

# IPs publicas de los Workers y el Master
WORKERS=("172.31.30.0" "172.31.17.157" "172.31.24.51" "172.31.27.79")
MASTER="172.31.30.146"

# User de el Master y los Workers
USER="ubuntu"
HOME="/home/$USER"

# Ubicacion de la llave privada
KEY="$HOME/.ssh/llave.pem"

# Variables de Entorno
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games..."
JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
HADOOP_HOME="/home/ubuntu/hadoop-3.3.6"
HADOOP_COMMON_HOME="/home/ubuntu/hadoop-3.3.6"

# Path del archivo comprimido de Hadoop
HADOOP_ARCHIVE="/home/ubuntu/hadoop-3.3.6.tar.gz"

# Ubicacion de las Variables de Entorno
ENV_VARS="/etc/environment"

for WORKER in "${WORKERS[@]}"; do
    echo ">>> Configurando al Worker de IP $WORKER <<<"

    echo ""
    echo "1) Instalando llave publica del Master en el Worker"
        MASTER_KEY="$(cat ~/.ssh/id_rsa.pub)"
    echo " > ssh $USER@$WORKER -i $KEY echo $MASTER_KEY >> ~/.ssh/authorized_keys"
    ssh $USER@$WORKER -i $KEY "echo $MASTER_KEY >> ~/.ssh/authorized_keys"

    echo ""
    echo "2) Creando llave publica para el Worker"
    echo " > ssh $USER@$WORKER -i $KEY ssh-keygen -t rsa"
    ssh $USER@$WORKER -i $KEY "ssh-keygen -t rsa"
    echo ""

    echo ""
    echo "3) Instalando llave del Worker en el Master"
    echo " > ssh $USER@$WORKER -i $KEY cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys"
    ssh $USER@$WORKER -i $KEY "cat ~/.ssh/id_rsa.pub" >> ~/.ssh/authorized_keys
    echo ""

    echo ""
    echo "4) Instalando llave del Worker en el mismo Worker"
    echo " > ssh $USER@$WORKER cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys"
    ssh $USER@$WORKER "cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys"
    echo ""

    echo ""
    echo "5) Actualizando sistema operativo en el Worker"
    echo " > ssh $USER@$WORKER sudo apt update -qq && sudo apt upgrade -y -qq"
    ssh $USER@$WORKER "sudo apt update -qq && sudo apt upgrade -y -qq"
    echo ""
...