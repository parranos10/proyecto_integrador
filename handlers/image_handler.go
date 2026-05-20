package handlers

import (
	"fmt"
	"net/http"
)

func Home(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Sistema gestión de imagenes")
}

func GetImages(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Lista imagenes")
}
