# -------------------------------------------------------------------
# Terraform module to deploy an EKS (Elastic Kubernetes Service) cluster
# -------------------------------------------------------------------
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.8.4"

  cluster_name    = local.cluster_name
  cluster_version = var.kubernetes_version
  subnet_ids      = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id
  enable_irsa     = true

  tags = {
    cluster = "demo"
  }

  # Optional: Disable GPU/inference blocks that may be breaking your plan
  manage_aws_auth_configmap = true

  eks_managed_node_group_defaults = {
    ami_type               = "AL2_x86_64"
    instance_types         = ["t3.large"]
    vpc_security_group_ids = [aws_security_group.all_worker_mgmt.id]

    # Workaround to prevent invalid block generation in the launch template
    # You can omit this section entirely if not using GPU-enabled nodes
    # launch_template = {
    #   id = "replace-with-launch-template-id"
    # }
  }

  eks_managed_node_groups = {
    node_group = {
      min_size     = 2
      max_size     = 6
      desired_size = 2
    }
  }
}
