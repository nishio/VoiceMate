tell application "Notes"
    tell account "iCloud"
        make new note with properties {body:"{content}"}
    end tell
end tell
