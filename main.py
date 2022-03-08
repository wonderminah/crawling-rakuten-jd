import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import markdown
import xlsxwriter

# URL
url = 'https://japan-job-en.rakuten.careers/search-jobs/data%20analyst/'

# chrome-driverを起動、クローリング
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get(url)

# excelファイルに書き出し関連
# workbook = xlsxwriter.Workbook('crawling_result.xlsx')
# worksheet = workbook.add_worksheet()

# htmlファイルに書き出し関連
file = open('crawling_result.html', 'w', encoding='UTF-8')
file.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Crawling Result - Search our Job Opportunities at Rakuten</title>
</head>
<body>
<table>
    <tbody>
""")

# 返却対象配列とカウント
crawlingResult = {}
totalCount = 0

# 終了フラグ
terminate = False

# 繰り返し文スタート
while not terminate:
    # リストを読み込み
    print('リストを読み込み')
    # driver.implicitly_wait(10)
    # searchResult = driver.find_element(By.ID, 'search-results-list')
    # jobList = searchResult.find_elements(By.CSS_SELECTOR, 'ul > li > a')
    jobList = driver.find_elements(By.CSS_SELECTOR, '#search-results-list > ul > li > a')

    print('총' + str(len(jobList)) + '개의 요소가 확인 되었습니다.')

    # リストで繰り返し
    for idx, job in enumerate(jobList):
        totalCount = totalCount + 1
        print(str(totalCount) + '번째 요소 취득을 시작합니다.')

        jobTitle = job.find_element(By.TAG_NAME, 'h2').text
        jobUrl = job.get_attribute('href')
        jobLocation = job.find_element(By.CSS_SELECTOR, 'span.job-location').text.replace('Location: ', '')
        jobCategory = job.find_element(By.CSS_SELECTOR, 'span.job-category').text.replace('Category: ', '')

        newTabDriver = webdriver.Chrome()
        newTabDriver.implicitly_wait(10)
        newTabDriver.get(jobUrl)
        jobDescription = newTabDriver.find_element(By.ID, 'richTextArea.jobPosting.jobDescription-input').text
        jobDescription = markdown.markdown(jobDescription, extensions=['nl2br'])
        print(jobDescription)

        # htmlに書き出し
        file.write('<tr><td><a href="' + jobUrl + '"><b>' + jobTitle + '</b></a></td></tr>')
        file.write('<tr><td>' + jobLocation + '</td></tr>')
        file.write('<tr><td>' + jobCategory + '</td></tr>')
        file.write('<tr><td>' + jobDescription + '</td></tr>')

        # dictに返却
        # crawlingResult[totalCount] = {
        #     'Title': jobTitle,
        #     'Url': jobUrl,
        #     'Location': jobLocation,
        #     'Category': jobCategory
        # }

        # 最後の要素に到達した場合
        if (idx + 1) == len(jobList):
            print('最後の要素に到達した場合')

            # 次のページが存在するかしないかを、nextボタンの存在で判断
            nextBtn = driver.find_element(By.CSS_SELECTOR, '#pagination-bottom > div.pagination-paging > a.next')
            nextBtnClass = nextBtn.get_attribute('class')

            # 次のページが存在する場合
            if nextBtnClass == 'next':
                print('nextBtn.click()')
                driver.execute_script("arguments[0].click();", nextBtn)
                time.sleep(2)
                break
            # 次のページが存在しない場合
            elif nextBtnClass == 'next disabled':
                terminate = True

print(crawlingResult)
file.write("""
</tbody>
</table>
</body>
</html>
""")

# レスポンス
# response = requests.get(url)
# クローリング結果を返却する配列を定義
# crawlingResult = {}

# # レスポンスが200の場合
# if response.status_code == 200:
#     html = response.text
#     soup = BeautifulSoup(html, 'html.parser')
#     searchResults = soup.select_one('#search-results-list')
#     jobList = searchResults.select('li > a')
#     # <a>タグ区切りで繰り返し処理
#     for idx, el in enumerate(jobList):
#         num = idx + 1
#         print(str(num) + "/" + str(len(jobList)))
#         print(el.h2.text)
#         print(el.get('href'))
#         print(el.select_one('span.job-location').text)
#         print(el.select_one('span.job-category').text)
#         print('\n')
#         # 一覧の最後要素に到達した場合
#         if num == len(jobList):
#             print('最後')
#             nextBtn = browser.find_element_by_css_selector('#pagination-bottom > div.pagination-paging > a.next')
#             nextBtn.click()
#
# # レスポンスが200以外の場合
# else:
#     print(response.status_code)
