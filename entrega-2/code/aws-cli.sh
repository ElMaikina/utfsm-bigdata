# Instalacion de AWS CLI

# Descargar archivo comprimido
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
# Descomprimir
unzip awscliv2.zip
# Instalar
sudo ./aws/install

# Descargar el CSV indicado
aws s3 cp s3://utfsm-inf356-dataset/vlt_observations_000.csv vlt_observations_000.csv --no-sign-request