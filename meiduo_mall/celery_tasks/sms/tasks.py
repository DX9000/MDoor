from rest_framework import status

from .yuntongxun.sms import CCP
import logging
from celery_tasks.main import celery_app

logger = logging.getLogger('django')

@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code, expires, SMS_CODE_TEMP_ID):
    try:
        ccp = CCP()
        # expires = constants.SMS_CODE_REDIS_EXPIRES // 60
        resule = ccp.send_template_sms(mobile, [sms_code, expires], SMS_CODE_TEMP_ID)
    except Exception as e:
        logger.error('验证码发送异常[异常]mobile:%s message:%s' % (mobile, e))

    else:
        if resule == 0:
            logging.info('短信验证码发送正常 moblie:%s' % mobile)

        else:
            logging.warning('短信发送失败 mobile：%s' % mobile)
