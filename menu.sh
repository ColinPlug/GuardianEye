#!/bin/bash

clear

while true; do
    echo "=============================="
    echo "GUARDIAN EYE - CONTROL PANEL"
    echo "=============================="
    echo "Selecteer een optie:"
    echo " ------------------------------"
    echo " 1) Main Pipeline (Batch Image Processing & Blurring) (Zorg voor Afbeeldingen in satellietbeelden)"
    echo " 2) Systeem Evaluatie (Metrics en MAE) (Zorg voor Afbeeldingen in satellietbeelden_test)"
    echo " 3) Interceptie Simulatie (Civilian Identificatie) (Uitgevoerd op Resultaten Stap 1)"
    echo " 4) Visualisatie Genereren (Grafieken) (Uitgevoerd op Resultaten Stap 1 en Stap 2)"
    echo ""
    echo " --- Test Dataset Utiliteiten ---"
    echo " 5) Genereer een Nieuwe Test Dataset (Sampler) (Zorg dat satellietbeelden_test Leeg is en verander Sample Size)"
    echo " 6) Sorteer de Ground Truth JSON (Order Fix)"
    echo ""
    echo " 7) Programma Verlaten"
    echo " ------------------------------"
    read -p "Selecteer een optie: " choice

    case $choice in
        1)  
            echo "Starten van de Main Pipeline..."
            python main.py
            ;;
        2)
            echo "Starten van de Systeem Evaluatie..."
            python evaluation/fase4_evaluation.py
            ;;
        3)
            echo "Starten van de Interceptie Simulatie..."
            python evaluation/fase5_interception.py
            ;;
        4)
            echo "Starten van de Visualisatie Genereren..."
            python evaluation/fase6_visualization.py
            ;;
        5)
            echo "Nieuwe Test Dataset Genereren..."
            python evaluation/fase4_sampler.py
            echo "Vergeet Niet om de ground_truth.json in te vullen"
            ;;
        6)
            echo "JSON Order van de Nieuwe Dataset Fixen..."
            python evaluation/fase4_json_order_fix.py
            ;;
        7)
            echo "Verlaten..."
            exit 0
            ;;
        *)
            echo "Ongeldige optie, probeer opnieuw."
            ;;
    esac

    echo ""
    read -p "Druk op Enter om terug te keren naar het hoofdmenu..."
    clear
done