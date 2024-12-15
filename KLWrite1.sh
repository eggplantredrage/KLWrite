#!/bin/bash

# KLWrite: An Open Source Text Editor in Shell Script

# Displays menu
display_menu() {
    echo "--------- KLWrite 0.1 ---------"
    echo "Menu"
    echo "1. Create a new file"
    echo "2. Edit an existing file"
    echo "3. View a file"
    echo "4. Exit Program"
    echo "-------------------------------"
}

# Create File
create_file() {
    read -p "Enter the filename to create: " filename
    if [ -f "$filename" ]; then
        echo "File already exists."
    else
        echo "KLWrite 0.1 - New Text File. Press Ctrl+D when you are done."
        cat > "$filename"
        echo "File created successfully."
    fi
}

# Edit File
edit_file() {
    read -p "Enter the filename to edit: " filename
    if [ ! -f "$filename" ]; then
        echo "File can't be found."
    else
        echo "KLWrite 0.1 - Editing $filename. Press Ctrl+D when you are done."
        echo "------- Existing Content -------"
        cat "$filename"
        echo "--------------------------------"
        cat >> "$filename"
        echo "File edited successfully."
    fi
}

# View File
view_file() {
    read -p "Enter the filename to view: " filename
    if [ ! -f "$filename" ]; then
        echo "File not found."
    else
        echo "Contents of $filename:"
        cat "$filename"
    fi
}

# Main program loop
while true; do
    display_menu
    read -p "Choose an option [1-4]: " choice
    case $choice in
        1) create_file ;;
        2) edit_file ;;
        3) view_file ;;
        4) 
            echo "Exiting KLWrite by Kevin Leblanc (Eggplant48). Thank you for using KLWrite!" 
            exit 0
            ;;
        *) echo "Invalid option. Please try again." ;;
    esac
done
