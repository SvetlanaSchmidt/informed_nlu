import argparse
import datetime
import logging
import os

import yaml

from fluidml import Flow
from fluidml.flow import TaskSpec, GridTaskSpec

from informed_nlu import project_path
from informed_nlu.tasks import (
    Parsing,
    Tokenisation,
    Pretraining,
    Training,
)
from informed_nlu.utils.fluid_helper import (
    configure_logging,
    MyLocalFileStore,
    TaskResource,
)
from informed_nlu.utils.training_utils import get_balanced_devices

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default=os.path.join(project_path, "configs", "config.yaml"),
        type=str,
        help="Path to config",
    )
    parser.add_argument(
        "--cuda-ids",
        default=None,
        type=int,
        nargs="+",
        help="GPU ids, e.g. `--cuda-ids 0 1`",
    )
    parser.add_argument("--use-cuda", action="store_true", help="Use cuda.")
    parser.add_argument("--warm-start", action="store_true", help="Tries to warm start training.")
    parser.add_argument("--num-workers", type=int, default=1, help="Number of multiprocessing workers.")
    parser.add_argument(
        "--force",
        type=str,
        nargs="+",
        default=None,
        help="Task or tasks to force execute. " + " registers successor tasks also for force execution."
        "E.g. --force ModelTraining+",
    )
    parser.add_argument(
        "--gs-expansion-method",
        type=str,
        default="product",
        choices=["product", "zip"],
        help="Method to expand config for grid search",
    )
    parser.add_argument("--log-to-tmux", action="store_true", help="Log to several tmux panes.")
    parser.add_argument(
        "--project-name",
        type=str,
        default="Contradiction_detection",
        help="Name of project.",
    )
    parser.add_argument("--run-name", type=str, default=None, help="Name of run.")
    return parser.parse_args()


def main():
    args = parse_args()
    config = yaml.safe_load(open(args.config, "r"))

    base_dir = config["base_dir"]

    # Parse run settings from argparse (defaults and choices see above in argparse)
    num_workers = args.num_workers  # 1
    force = args.force  # "ModelTraining+"
    use_cuda = args.use_cuda
    cuda_ids = args.cuda_ids  # [1]  # [0, 1]
    warm_start = args.warm_start  # False  # continue training from an existing checkpoint
    gs_expansion_method: str = args.gs_expansion_method

    log_dir = os.path.join(base_dir, "logging")
    os.makedirs(log_dir, exist_ok=True)
    configure_logging(level="INFO", log_dir=log_dir)

    # get task configs
    parsing_cfg = config["Parsing"]
    tokenisation_cfg = config["Tokenisation"]
    pretraining_cfg = config["Pretraining"]
    training_cfg = config["Training"]

    # training_additional_kwargs = {
    #     "checkpointer_params": {"serialization_dir": "models", "num_serialized_models_to_keep": 1},
    #     "train_logger_params": {
    #         "type_": "tensorboard",
    #         "log_dir": "logs",
    #     },
    #     "warm_start": warm_start,
    # }

    # create all task specs
    parsing = TaskSpec(task=Parsing, config=parsing_cfg)
    tokenisation = TaskSpec(task=Tokenisation, config=tokenisation_cfg)
    pretraining = TaskSpec(task=Pretraining, config=pretraining_cfg)
    training = GridTaskSpec(
        task=Training,
        gs_config=training_cfg,
        gs_expansion_method=gs_expansion_method,
        # additional_kwargs=training_additional_kwargs,
    )

    # dependencies between tasks
    tokenisation.requires(parsing)
    pretraining.requires(tokenisation)
    training.requires([tokenisation, pretraining])

    # list of all tasks
    tasks = [parsing, tokenisation, pretraining, training]

    # create list of resources
    devices = get_balanced_devices(count=num_workers, use_cuda=use_cuda, cuda_ids=cuda_ids)
    resources = [TaskResource(device=devices[i]) for i in range(num_workers)]

    # create local file storage used for versioning
    results_store = MyLocalFileStore(base_dir=base_dir)

    start = datetime.datetime.now()
    # create flow (expanded task graph)
    flow = Flow(tasks=tasks)
    # run linearly without swarm if num_workers is set to 1
    # note resources are now assigned equally to all tasks (e.g. device info)
    # else run graph in parallel using multiprocessing
    # create list of resources which is distributed among workers
    # e.g. to manage that each worker has dedicated access to specific gpus
    flow.run(
        num_workers=args.num_workers,
        resources=resources,
        log_to_tmux=args.log_to_tmux,
        force=args.force,
        results_store=results_store,
        project_name=args.project_name,
        run_name=args.run_name,
    )

    end = datetime.datetime.now()
    logger.info(f"{end - start}")


if __name__ == "__main__":
    main()
