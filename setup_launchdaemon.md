1. `sudo nano /Library/LaunchDaemons/com.coredev.start.plist`

    ```xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.coredev.start</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/turtle/projects/tools/core-dev/start_core.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
    ```

1. Set permissions

    ```shell
    sudo chown root:wheel /Library/LaunchDaemons/com.coredev.start.plist
    sudo chmod 644 /Library/LaunchDaemons/com.coredev.start.plist
    ```

1. Start Daemon: `sudo launchctl load /Library/LaunchDaemons/com.coredev.start.plist`

1. Check logs: `sudo log show --predicate 'eventMessage contains "com.coredev.start"' --info`
