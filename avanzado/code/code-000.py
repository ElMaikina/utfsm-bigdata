
583:/home/ubuntu/.local/share/pipx/venvs/flintrock/lib/python3.12/site-packages/flintrock/core.py 
    install_adoptium_repo(client)
    ssh_check_output(
        client=client,
        command="""
            set -e
            # Install dependencies manually (minimal GUI/headless support)
            sudo yum install -y \\
                alsa-lib \\
                dejavu-sans-fonts \\
                fontconfig \\
                libX11 \\
                libXext \\
                libXi \\
                libXrender \\
                libXtst
            echo "Getting temurin"
            wget https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.27%2B6/OpenJDK11U-jdk_x64_linux_hotspot_11.0.27_6.tar.gz -O /tmp/temurin11.tar.gz
            cd /opt
            sudo tar -xzf /tmp/temurin11.tar.gz
            sudo mv jdk-11.0.27+6 temurin-11
            # Set JAVA_HOME
            echo 'export JAVA_HOME=/opt/temurin-11' | sudo tee /etc/profile.d/java.sh
            echo 'export PATH=$JAVA_HOME/bin:$PATH' | sudo tee -a /etc/profile.d/java.sh
            source /etc/profile.d/java.sh
            # Verify
            java -version
            sudo yum remove -y java-1.6.0-openjdk java-1.7.0-openjdk
            sudo sh -c "echo export JAVA_HOME=/usr/lib/jvm/{jp} >> /etc/environment"
            source /etc/environment
        """)

38:/home/ubuntu/.local/share/pipx/venvs/flintrock/lib/python3.12/site-packages/flintrock/scripts/download-package.py
subprocess.check_call(['aws', 's3', 'cp', '--no-sign-request', url, download_path])
