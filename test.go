package main

import (
	"fmt"
	"io"
	"net/http"
	"time"
)

func main() {

	url := "http://localhost:8088/health"

	req, _ := http.NewRequest("GET", url, nil)

	tr := &http.Transport{
		MaxIdleConns:       10,
		IdleConnTimeout:    600 * time.Second,
		DisableCompression: true,
	}
	client := &http.Client{Transport: tr}

	res, err := client.Do(req)

	if err != nil {
		fmt.Printf("error:%e\n", err)
	}

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
