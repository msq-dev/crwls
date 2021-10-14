if __name__ == "__main__":
    import os
    from pathlib import Path
    from urllib.parse import urlparse
    import smtplib
    from email.message import EmailMessage
    import conf.config as config
    from crawl import crawl
    from compare import compare

    with open(config.URLS_LIST, "r") as file:
        urls = list(file)
        for url in urls:
            task_name = urlparse(url).netloc
            if not Path(f"{config.OUTPUT_PATH}{task_name}").exists():
                os.mkdir(Path(config.OUTPUT_PATH) / task_name)

            crawl(url, task_name)
            changes = compare(task_name)

            if changes:
                with open(f"{config.CHANGES_PATH}changes_{task_name}.html", "w") as change_file:
                    change_file.write(changes)
                print(f"{task_name}: Yes changes")
            else:
                print(f"{task_name}: No changes")

            if changes and config.MAIL_MODE:
                msg = EmailMessage()
                msg.set_content(changes)
                msg["Subject"] = "Hallo Changes"
                msg["From"] = config.GMAIL_USER
                msg["To"] = config.GMAIL_USER

                try:
                    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                    server.login(config.GMAIL_USER, config.GMAIL_PASSWORD)
                    server.send_message(msg)
                    print("Email sent")
                    server.quit()
                except Exception as error:
                    print(error)

            else:
                print("No Email")
