# Run: source ./activate_lab.sh
LAB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-${(%):-%N}}")" && pwd)"
source "$LAB_ROOT/.venv/bin/activate"
export YOLO_CONFIG_DIR="$LAB_ROOT/work/runtime/ultralytics"
export MPLCONFIGDIR="$LAB_ROOT/work/runtime/matplotlib"
export HF_HOME="$LAB_ROOT/models/huggingface"
export PYTORCH_ENABLE_MPS_FALLBACK=1
export YOLO_AUTOINSTALL=false
unset LAB_ROOT
