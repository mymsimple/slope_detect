if [ "$1" = "help" ]; then
    echo "pb_pred.sh 使用说明：
    --image_dir     被预测的图片目录
    --pred_dir      预测后的结果的输出目录
    --model_dir     model的存放目录，会自动加载最新的那个模型
    --model_file    model的模型文件 "
    exit
fi

echo "开始检测图片的倾斜....."

python pb_pred.py \
    --gpu=0 \
    --image_name=$1 \
    --pred_dir=data/validate \
    --debug=True \
    --model_dir=model/pb/100000