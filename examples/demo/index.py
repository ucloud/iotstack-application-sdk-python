import json
import logging
import time

from iotedgeapplicationlinksdk import getLogger
from iotedgeapplicationlinksdk.client import get_application_config, get_application_name, get_gateway_product_sn, get_gateway_device_sn, publish, register_callback

# 配置log
log = getLogger()
log.setLevel(logging.DEBUG)

# 主函数
if __name__ == "__main__":
    try:
        # 获取应用配置信息
        appConfig = get_application_config()
        log.info('app config:{}'.format(appConfig))

        # 从应用配置获取设备数据上报周期
        uploadPeriod = 5
        if "period" in appConfig.keys() and isinstance(appConfig['period'], int):
            uploadPeriod = int(appConfig['period'])

        appName = get_application_name()
        productSN = get_gateway_product_sn()
        deviceSN = get_gateway_device_sn()
        log.info('app info:{}, {}, {}'.format(appName, productSN, deviceSN))

        # 设置应用上报topic
        topic = '/{}/{}/upload'.format(productSN, deviceSN)

        # 设置应用消息回调
        def callback(topic: str, payload: bytes):
            log.info("recv message from {} : {}".format(topic, str(payload)))

        # 设置应用RRPC消息回调
        def rrpc_callback(topic: str, payload: bytes):
            log.info("recv rrpc message from {} : {}".format(
                topic, str(payload)))

        register_callback(callback, rrpc_callback)
        i = 0
        # 周期上报消息
        while True:
            relayStatus = ("on", "off")[i % 2 == 0]
            payload = {
                "timestamp": time.time(),
                'RelayStatus': relayStatus
            }

            byts = json.dumps(payload).encode('utf-8')

            publish(topic, byts)

            log.info("upload {} : {}".format(topic, str(byts)))

            time.sleep(uploadPeriod)
            i = i+1
            if (i > 1000):
                i = 1

    except Exception as e:
        log.error('load app config error: {}'.format(str(e)))
        exit(1)
