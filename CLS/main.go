package main

import (
	"fmt"
	"net/http"

	// removed import of local routes package which was causing import error
)

func main() {

	// simple default route to avoid depending on external package
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Servidor iniciado")
	})

	fmt.Println("Servidor iniciado en puerto 8080")
	http.ListenAndServe(":8080", nil)
}
