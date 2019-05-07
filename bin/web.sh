CUDA_VISIBLE_DEVICES=0 gunicorn \
    web.server:app \
    --workers=1 \
    --worker-class=gevent \
    --bind=0.0.0.0:8080 \
    --timeout=300 \
    --model_dir=model \
    --model_file=ctpn-2019-05-07-14-19-35-201.ckpt