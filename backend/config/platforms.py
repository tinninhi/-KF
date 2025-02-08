PLATFORM_CONFIG = {
    "toutiao": {
        "login_url": "https://mp.toutiao.com/login/",
        "publish_xpath": {
            "title": "//textarea[@placeholder='请输入标题']",
            "content": "//div[@class='editor-container']"
        }
    },
    "baijia": {
        "login_url": "https://baijiahao.baidu.com/builder/rc/login",
        "publish_xpath": {
            "title": "//input[@placeholder='输入文章标题']",
            "content": "//div[@id='content-editor']"
        }
    }
}