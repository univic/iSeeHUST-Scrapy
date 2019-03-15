# /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : univic
# CreateDate : 2017-06-20

task_list = {
    'cm_xydt': (
        'http://cm.hust.edu.cn/', 'http://cm.hust.edu.cn/zz_xwzx/', 'xydt.htm', 'listmb', 'parser_cm', '管理学院', '学院动态'),
    'cm_xstz': (
        'http://cm.hust.edu.cn/', 'http://cm.hust.edu.cn/zz_xwzx/', 'xstz.htm', 'listmb', 'parser_cm', '管理学院', '学术通知'),
    'cm_tzgg': (
        'http://cm.hust.edu.cn/', 'http://cm.hust.edu.cn/zz_xwzx/', 'tzgg.htm', 'listmb', 'parser_cm', '管理学院', '通知公告'),
    'cm_yyld': (
        'http://cm.hust.edu.cn/', 'http://cm.hust.edu.cn/zz_xwzx/', 'yyld.htm', 'listmb', 'parser_cm', '管理学院', '喻园论道'),
    'cm_zxdt': (
        'http://cm.hust.edu.cn/', 'http://cm.hust.edu.cn/ss/', 'zxdt.htm', 'listmb', 'parser_cm', '管理学院', '硕士动态'),
    'cm_zsxx': (
        'http://cm.hust.edu.cn/', 'http://cm.hust.edu.cn/ss/', 'zsxx.htm', 'listmb', 'parser_cm', '管理学院', '招生信息'),
    'cm_jxgl': (
        'http://cm.hust.edu.cn/', 'http://cm.hust.edu.cn/ss/', 'jxgl.htm', 'listmb', 'parser_cm', '管理学院', '教学管理（研究生）'),
    'cm_xwsq': (
        'http://cm.hust.edu.cn/', 'http://cm.hust.edu.cn/ss/', 'xwsq.htm', 'listmb', 'parser_cm', '管理学院', '学位申请'),
    'cm_cc_zxdt': (
        'http://cm.hust.edu.cn/', 'http://cm.hust.edu.cn/MPAcc/xwdt/', 'zxdt.htm', 'listmb', 'parser_cm', '管理学院', 'MPAcc动态'),
    'cm_zpxx': (
        'http://cm.hust.edu.cn/', 'http://cm.hust.edu.cn/zyfz/', 'zpxx.htm', 'listmb', 'parser_cm', '管理学院', '招聘信息'),
    'cm_sxxx': (
        'http://cm.hust.edu.cn/', 'http://cm.hust.edu.cn/zyfz/', 'sxxx.htm', 'listmb', 'parser_cm', '管理学院', '实习信息'),
    'cm_zyfz': (
        'http://cm.hust.edu.cn/', 'http://cm.hust.edu.cn/zyfz/', 'zyfz.htm', 'listmb', 'parser_cm', '管理学院', '职业发展'),
    'gs_ksxx': (
        'http://gs.hust.edu.cn/', 'http://gs.hust.edu.cn/yjspy/', 'ksxx.htm', 'ctbody ctbder', 'parser_gs', '研究生院', '考试信息'),
    'gs_xkxx': (
        'http://gs.hust.edu.cn/', 'http://gs.hust.edu.cn/yjspy/', 'xkxx.htm', 'ctbody ctbder', 'parser_gs', '研究生院', '选课信息'),
    'gs_gjjl': (
        'http://gs.hust.edu.cn/', 'http://gs.hust.edu.cn/yjspy/', 'gjjlyhz.htm', 'ctbody ctbder', 'parser_gs', '研究生院', '国际交流'),
    'gs_tzgg': (
        'http://gs.hust.edu.cn/', 'http://gs.hust.edu.cn/', 'tzgg.htm', 'ctbody ctbder', 'parser_gs', '研究生院', '通知公告'),
    'gs_zsggtz': (
        'http://gszs.hust.edu.cn/', 'http://gszs.hust.edu.cn/zsxx/', 'ggtz.htm', 'main_conRCb', 'parser_gs', '研究生院', '招生通知公告'),
    'eco_xsdt': (
        'http://eco.hust.edu.cn/', 'http://eco.hust.edu.cn/xydt/', 'xsdt.htm', 'main_con', 'parser_eco', '经济学院',
        '学术动态')
}


APP_CONFIG = {
    'HARD_TIME_LIMITER': 10080,
    'HARD_AMOUNT_LIMITER': 15,
    'DB_SCHEMA': 'schema.sql',
    'FETCH_INTERVAL': 60,          # Default data fetch interval(minutes)
    'DEFAULT_DATE_RANGE': 30,      # Maximum date range displayed in Flask page
    'NIGHT_SHIFT': True,    # The app will run at a increased interval at night
    'WEEKEND_SHIFT': True,    # The app will run at a increased interval during weekend
    'OFFSHIFT_INTERVAL': 360,       # Data fetch interval during night and weekend(minutes)
    'SHIFT_START': 7,
    'SHIFT_END': 18,
    'MAX_LOG_SIZE': 512             # Max log size in KB
}

DB_CONFIGS = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'iSeeHUST',
    'charset': 'utf8'
}