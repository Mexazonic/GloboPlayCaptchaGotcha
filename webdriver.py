
## Este Script foi baseado no sistema de votação do BBB20
## Portanto Como as Votações estão encerradas não terá êxito em sua execução

import time
from selenium import webdriver
from undetected_chromedriver import Chrome, ChromeOptions

driver = Chrome()


#driver = webdriver.Firefox('/home/bruno/')
#driver = webdriver.Firefox(executable_path='/home/bruno/geckodriver')

login = 'your-email'
password = 'your-pass'

driver.get("https://login.globo.com/login/1")
login = driver.find_element_by_id("login").send_keys(login)
time.sleep(3)



login = driver.find_element_by_id("password").send_keys(password)

time.sleep(2)


submit = driver.find_elements_by_xpath('//*[@id="login-form"]/div[6]/button')

time.sleep(2)
submit[0].click()



link = 'https://gshow.globo.com/realities/bbb/bbb20/votacao/paredao-bbb20-quem-voce-quer-eliminar-babu-rafa-ou-thelma-0ffab592-8b60-42aa-b29f-ff828805e7ed.ghtml'
driver.get(link)

time.sleep(3)

enemy = '//*[@id="roulette-root"]/div/div[1]/div[4]/div[3]/div/div[1]'


submit = driver.find_elements_by_xpath(enemy)

time.sleep(2)

submit[0].click()
 

driver.execute_script("window.scrollTo(0, 1800)") 

image_enemy = '//*[@id="roulette-root"]/div/div[1]/div[4]/div[3]/div[2]/div/div/div[2]/div/div[2]/img'
time.sleep(3)

n = 1
count = 0
lost = 0
while True:
    
    try:
        time.sleep(10)    
        vote = driver.find_elements_by_xpath(image_enemy)
        time.sleep(2)
        vote[0].click()
        lost += 1
        print("voted")

        #time.sleep(15)
    
    except:

        driver.get(link)
        time.sleep(5)
        submit = driver.find_elements_by_xpath(enemy)
        #time.sleep(2)
        submit[0].click()
        driver.execute_script("window.scrollTo(0, 2000)") 
        count += 1
        print("votos efetuados: %d" % count)

