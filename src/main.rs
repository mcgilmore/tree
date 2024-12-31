use clap::{Arg, Command};
use csv::ReaderBuilder;
use reqwest;
use std::collections::HashSet;
use std::fs;
use std::fs::File;
use std::io::{self, Write};
use webbrowser;

fn fetch_data(group_id: &str) -> Result<String, reqwest::Error> {
    let url = format!("https://data.orthodb.org/current/tab?id={}", group_id);
    let response = reqwest::blocking::get(&url)?;

    if response.status().is_success() {
        let text = response.text()?;
        // Return everything after the third newline (header and metadata removed)
        Ok(text.splitn(4, '\n').nth(3).unwrap_or("").to_string())
    } else {
        Err(reqwest::blocking::get(&url)?
            .error_for_status()
            .unwrap_err())
    }
}

fn blast_sequence(sequence: &str) -> Result<String, reqwest::Error> {
    let url = format!("https://data.orthodb.org/v12/blast?seq={}", sequence);
    let response = reqwest::blocking::get(&url)?;

    if response.status().is_success() {
        Ok(response.text()?)
    } else {
        Err(response.error_for_status().unwrap_err())
    }
}

fn parse_organism_names(data: &str) -> Vec<String> {
    let mut reader = ReaderBuilder::new()
        .delimiter(b'\t')
        .from_reader(data.as_bytes());
    let mut organism_names = Vec::new();

    for result in reader.records() {
        if let Ok(record) = result {
            if let Some(organism_name) = record.get(4) {
                organism_names.push(organism_name.replace(" ", "_"));
            }
        }
    }

    // Remove duplicates
    let unique_names: HashSet<_> = organism_names.into_iter().collect();
    unique_names.into_iter().collect()
}

fn write_itol(file_path: &str, unique_names: &[String], group_id: Option<&str>) -> io::Result<()> {
    let mut file = File::create(file_path)?;
    writeln!(file, "DATASET_GRADIENT")?;
    writeln!(file, "#Dataset created using tree.rs\n")?;
    writeln!(file, "SEPARATOR TAB")?;
    writeln!(
        file,
        "DATASET_LABEL\t{}",
        group_id.unwrap_or("Unknown Group")
    )?;
    writeln!(file, "COLOR\t#00ff00")?;
    writeln!(file, "COLOR_MIN\t#00ff00")?;
    writeln!(file, "COLOR_MAX\t#0000ff\n")?;
    writeln!(file, "DATA")?;

    for organism_name in unique_names {
        writeln!(file, "{}\t1", organism_name)?;
    }

    Ok(())
}

fn main() {
    let matches = Command::new("iTOL Dataset Generator")
        .version("1.0")
        .author("Michael Gilmore <michael_gilmore@live.com>")
        .about("Generates iTOL dataset files from OrthoDB data")
        .arg(
            Arg::new("group_id")
                .short('g')
                .long("group_id")
                .help("An orthoDB group ID to fetch data for")
                .required(false)
                .value_name("TEXT"),
        )
        .arg(
            Arg::new("output")
                .short('o')
                .long("output")
                .help("Specify the output file")
                .value_name("FILE"),
        )
        .arg(
            Arg::new("open-orthodb")
                .short('d')
                .long("open-orthodb")
                .help("Open OrthoDB in the default browser")
                .action(clap::ArgAction::SetTrue),
        )
        .arg(
            Arg::new("blast")
                .short('b')
                .long("blast")
                .help("Provide a protein sequence in FASTA format to blast against OrthoDB")
                .value_name("FASTA_FILE"),
        )
        .get_matches();

    let group_id = matches.get_one::<String>("group_id");
    let output_file = matches.get_one::<String>("output");
    let blast_file = matches.get_one::<String>("blast");
    
    if matches.get_flag("open-orthodb") {
        if webbrowser::open("https://www.orthodb.org/").is_err() {
            eprintln!("Could not open OrthoDB in your default browser.");
            std::process::exit(1);
        } else {
            println!("Opened OrthoDB in your browser");
            return;
        }
    }

    if let Some(blast_path) = blast_file {
        match fs::read_to_string(blast_path) {
            Ok(sequence) => {
                match blast_sequence(&sequence.trim()) {
                    Ok(response) => {
                        println!("BLAST response: {}", response);
                        // Additional processing of the JSON response can be done here
                    }
                    Err(e) => {
                        eprintln!("Error blasting sequence: {}", e);
                        std::process::exit(1);
                    }
                }
            }
            Err(e) => {
                eprintln!("Error reading blast file: {}", e);
                std::process::exit(1);
            }
        }
    }

    if let Some(group_id) = group_id {
        println!("Using {} as input", group_id);

        match fetch_data(group_id) {
            Ok(data) => {
                let organism_names = parse_organism_names(&data);
                let default_file_path = format!("{}.txt", group_id);
                let file_path = output_file.unwrap_or(&default_file_path);

                if let Err(e) = write_itol(file_path, &organism_names, Some(group_id)) {
                    eprintln!("Error writing file: {}", e);
                    std::process::exit(1);
                }

                println!("File written successfully to {}", file_path);
            }
            Err(e) => {
                eprintln!("Error fetching data: {}", e);
                std::process::exit(1);
            }
        }
    } else {
        println!("No group ID provided. Use --help for usage information");
    }
}
