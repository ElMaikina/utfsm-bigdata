...
    echo ""
    echo "6) Instalando Java en el Worker"
    echo " > ssh $USER@$WORKER sudo apt-get install -y -qq openjdk-11-jdk"
    ssh $USER@$WORKER "sudo apt-get install -y -qq openjdk-11-jdk"
    echo ""

    echo ""
    # Esta seccion me dio problemas asi que este paso lo hice manual al final
    echo "7) Copiando las Variables de Entorno en el Worker"
        echo " > cat $HOME/environment"
        cat $HOME/environment
    echo " > scp $HOME/environment $USER@$WORKER:$HOME/"
    scp $HOME/environment $USER@$WORKER:$HOME/
    echo "ssh $USER@$WORKER cat $HOME/enviroment"
    ssh $USER@$WORKER "cat $HOME/enviroment"
    echo " > ssh $USER@$WORKER sudo cp $HOME/enviroment $ENV_VARS"
    ssh $USER@$WORKER "sudo cp $HOME/enviroment $ENV_VARS"
    echo " > ssh $USER@$WORKER cat $ENV_VARS"
    ssh $USER@$WORKER "cat $ENV_VARS"

    echo ""

    echo ""
    echo "8) Copiando archivo de despliegue Hadoop al Worker..."
    echo "ssh $USER@$WORKER rm $HADOOP_ARCHIVE && ls -la"
    ssh $USER@$WORKER "rm $HADOOP_ARCHIVE && ls -la"
    echo " > scp $HADOOP_ARCHIVE $USER@$WORKER:$HOME/"
    scp $HADOOP_ARCHIVE $USER@$WORKER:$HOME/
    echo " > ssh $USER@$WORKER ls -la"
    ssh $USER@$WORKER "ls -la"
    echo ""

    echo ""
    echo "9) Descomprimiendo el archivo de despliegue en el Worker..."
    echo " > ssh $USER@$WORKER tar -xzf $HADOOP_HOME.tar.gz -C $HOME/"
    ssh $USER@$WORKER "tar -xzf $HADOOP_HOME.tar.gz -C $HOME/"
    echo ""

    echo ""
    echo "10) Reiniciando Worker..."
    echo " > ssh $USER@$WORKER sudo reboot now"
    ssh $USER@$WORKER "sudo reboot now"
    echo ""

    echo "El Worker de IP $WORKER ha sido configurado correctamente! :)"
    echo ""
done

echo "Todos los Workers han sido configurados! :D"