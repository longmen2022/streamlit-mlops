# STEP1: CREATE SG
resource "aws_security_group" "my-sg" {
  name        = "JENKINS-SERVER-SG"
  description = "Jenkins Server Ports"

  # Port 22 is required for SSH Access
  ingress {
    description = "SSH Port"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 80 is required for HTTP
  ingress {
    description = "HTTP Port"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 443 is required for HTTPS
  ingress {
    description = "HTTPS Port"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 2379-2380 is required for etcd-cluster
  ingress {
    description = "etc-cluster Port"
    from_port   = 2379
    to_port     = 2380
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 3000 is required for Grafana
  ingress {
    description = "NPM Port"
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 6443 is required for KubeAPIServer
  ingress {
    description = "Kube API Server"
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 8080 is required for Jenkins
  ingress {
    description = "Jenkins Port"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 9000 is required for SonarQube
  ingress {
    description = "SonarQube Port"
    from_port   = 9000
    to_port     = 9000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 9090 is required for Prometheus
  ingress {
    description = "Prometheus Port"
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 9100 is required for Prometheus metrics server
  ingress {
    description = "Prometheus Metrics Port"
    from_port   = 9100
    to_port     = 9100
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 10250-10260 is required for K8s
  ingress {
    description = "K8s Ports"
    from_port   = 10250
    to_port     = 10260
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Port 30000-32767 is required for NodePort
  ingress {
    description = "K8s NodePort"
    from_port   = 30000
    to_port     = 32767
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Define outbound rules to allow all
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}