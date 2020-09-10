package main

import (
	"encoding/json"
	"fmt"
)

type Book struct {
	Title  string `json:"title"`
	Author Author `json:"author"`
}

type Author struct {
	Sales     int  `json:"book_sales"`
	Age       int  `json:"age"`
	Developer bool `json:"is_developer"`
}

var example = map[string]int{
	"a": 1,
	"b": 2,
}

func main() {
	author := Author{Sales: 3, Age: 25, Developer: true}
	book := Book{Title: "Learning Concurrency in Python", Author: author}

	text, err := json.Marshal(example)
	if err != nil {
		fmt.Println(err)
	}

	byteArray, err := json.MarshalIndent(book, "", " ")
	if err != nil {
		fmt.Println(err)
	}

	fmt.Println(string(text))
	fmt.Println(string(byteArray))

}