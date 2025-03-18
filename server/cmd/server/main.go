package main

import (
	"database/sql"
	"flag"
	"log"
	"net/http"

	_ "github.com/mattn/go-sqlite3"
)

func main() {
	var addr string
	var dbPath string
	flag.StringVar(&addr, "addr", ":8080", "address to listen on")
	flag.StringVar(&dbPath, "db", "db.sqlite3", "path to the database file")
	flag.Parse()

	db, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	_, err = db.Exec("CREATE TABLE IF NOT EXISTS heart_rate (measured_time TEXT, heart_rate INTEGER, rr_intervals TEXT)")
	if err != nil {
		log.Fatal(err)
	}

	mux := http.NewServeMux()
	mux.HandleFunc("POST /", func(w http.ResponseWriter, r *http.Request) {
		err := r.ParseForm()
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		measuredTime := r.FormValue("measured_time")
		heartRate := r.FormValue("heart_rate")
		rrIntervals := r.FormValue("rr_intervals")
		_, err = db.Exec("INSERT INTO heart_rate (measured_time, heart_rate, rr_intervals) VALUES (?, ?, ?)", measuredTime, heartRate, rrIntervals)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.WriteHeader(http.StatusCreated)
	})

	log.Fatal(http.ListenAndServe(addr, mux))
}
