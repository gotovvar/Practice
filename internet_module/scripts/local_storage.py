from utils.browser_setup import get_edge_driver


def main():
    driver = get_edge_driver()

    try:
        driver.get('https://example.com')

        driver.execute_script("window.localStorage.setItem('myKey', 'myValue');")

        value = driver.execute_script("return window.localStorage.getItem('myKey');")
        print(f"Value from LocalStorage: {value}")

        driver.execute_script("window.localStorage.removeItem('myKey');")

        value_after_deletion = driver.execute_script("return window.localStorage.getItem('myKey');")
        print(f"Value after deletion: {value_after_deletion}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
