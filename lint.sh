fill() {
    local text="$1"
    local fill_char="$2"
    local columns=$(tput cols)
    local stars=$(( (columns - ${#text}) / 2  - 1))
    printf '%.s*' $(seq 1 $stars) 
    printf " "
    printf $text
    printf " "
    printf '%.s*' $(seq 1 $stars)
    printf "\n"
}

fill "BLACK" "*"
poetry run black $1
fill "ISORT" "*"
poetry run isort $1
fill "MYPY" "*"
poetry run mypy $1
fill "FLAKE8" "*"
poetry run flake8 $1
fill "PYLINT" "*"
poetry run pylint $1