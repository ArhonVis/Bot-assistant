from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

def proc(st):
    i0 = st.find('Сегодня')
    i1 = st.find('днём')
    date = st[i0 + 7 : i1]
    if (date[1:].isalpha()):
        date = date[0] + ' ' + date[1:]
    else:
        date = date[:2] + ' ' + date[2:]
    i0 = i1 + 4
    i1 = st.find('ночью')
    t1 = st[i0 : i1]
    i0 = i1 + 5
    if (st[i0 + 4].isalpha()):
        t2 = st[i0: i0 + 4]
        end = st[i0 + 4:]
    else:
        t2 = st[i0 : i0 + 5]
        end = st[i0 + 5:]
    res = "Сегодня " + date + ' днём ' + t1 + ' ночью ' + t2 + ' ' + end
    return(res)
def get(position):
    opt = webdriver.ChromeOptions()
    opt.set_headless()
    driver = webdriver.Chrome(chrome_options=opt)
    driver.get("https://yandex.by/pogoda/moscow?via=hl" )
    elem = driver.find_element_by_name("request")
    elem.send_keys(position)
    elem.submit()
    elem = driver.find_elements_by_tag_name("li")
    if (len(elem) == 0):
        elem = driver.find_elements_by_tag_name("li")
    elem[0].click()
    time.sleep(3)
    driver.execute_script("console.clear();")
    driver.execute_script('let answ = []; let arr = document.getElementsByClassName("link link_theme_normal i-bem"); for (let i = 0; i<(arr.length-1); i++){answ.push(arr[i].textContent)} let arr2 = answ.toString();  let box = $("<p id = \'box\'>" + arr2 +" </p>"); $("body").append(box);')
    data = driver.find_element_by_id("box").text
    driver.close
    begin = data.find(",Сегодня")
    end = data.find(",", begin + 1, -1)
    res = data[begin + 1 : end]
    res = proc(res)
    driver.close
    return(res)
