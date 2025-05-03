import tkinter as tk
from tkinter import PhotoImage
import sqlite3
from datetime import datetime, timedelta
import requests
import webbrowser

# --- Database Initialization ---
DB_NAME = "plants.db"
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

try:
    c.execute("ALTER TABLE user_plants ADD COLUMN custom_name TEXT")
except sqlite3.OperationalError:
    pass

c.execute('''CREATE TABLE IF NOT EXISTS plants (
    id INTEGER PRIMARY KEY,
    name TEXT,
    scientific_name TEXT,
    watering TEXT,
    sunlight TEXT,
    height TEXT,
    flower_color TEXT,
    growth_rate TEXT,
    care_instructions TEXT,
    image_url TEXT,
    wikipedia_url TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS user_plants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plant_id INTEGER,
    latitude REAL,
    longitude REAL,
    next_water_time TEXT,
    custom_name TEXT,
    FOREIGN KEY(plant_id) REFERENCES plants(id)
)''')

plants = [
(1, "Aloe Vera", "Aloe barbadensis miller", "High", "Bright, indirect", "Up to 60 cm", "Green", "Slow", "Water when soil is dry", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Aloe_vera.jpg/320px-Aloe_vera.jpg", "https://en.wikipedia.org/wiki/Aloe_vera"),
(2, "Spider Plant", "Chlorophytum comosum", "Moderate", "Indirect light", "Up to 60 cm", "Green/White", "Moderate", "Water when soil is dry", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Spider_plant.jpg/320px-Spider_plant.jpg", "https://en.wikipedia.org/wiki/Chlorophytum_comosum"),
(3, "Snake Plant", "Sansevieria trifasciata", "Low", "Low to bright", "Up to 1 m", "Green", "Slow", "Water sparingly", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Sansevieria_trifasciata.jpg/320px-Sansevieria_trifasciata.jpg", "https://en.wikipedia.org/wiki/Sansevieria_trifasciata"),
(4, "Peace Lily", "Spathiphyllum", "Moderate", "Low to medium light", "Up to 1 m", "Green/White", "Moderate", "Water when soil is dry", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Spathiphyllum_bloom_3.jpg/320px-Spathiphyllum_bloom_3.jpg", "https://en.wikipedia.org/wiki/Spathiphyllum"),
(5, "ZZ Plant", "Zamioculcas zamiifolia", "Low", "Low to bright", "Up to 1 m", "Green", "Slow", "Water sparingly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Zamioculcas_zamiifolia.jpg/320px-Zamioculcas_zamiifolia.jpg", "https://en.wikipedia.org/wiki/Zamioculcas_zamiifolia"),
(6, "Pothos", "Epipremnum aureum", "Low", "Low to bright", "Up to 2 m", "Green/Yellow", "Moderate", "Water when soil is dry", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Pothos_%28Epipremnum_aureum%29.jpg/320px-Pothos_%28Epipremnum_aureum%29.jpg", "https://en.wikipedia.org/wiki/Epipremnum_aureum"),
(7, "Fiddle Leaf Fig", "Ficus lyrata", "High", "Bright, indirect", "Up to 3 m", "Green", "Slow", "Water when soil is dry", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Ficus_lyrata.jpg/320px-Ficus_lyrata.jpg", "https://en.wikipedia.org/wiki/Ficus_lyrata"),
(8, "English Ivy", "Hedera helix", "Low", "Low to bright", "Up to 30 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Hedera_helix_2018.jpg/320px-Hedera_helix_2018.jpg", "https://en.wikipedia.org/wiki/Hedera_helix"),
(9, "Dracaena", "Dracaena marginata", "Moderate", "Indirect light", "Up to 2 m", "Green", "Slow", "Water when soil is dry", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Dracaena_marginata.jpg/320px-Dracaena_marginata.jpg", "https://en.wikipedia.org/wiki/Dracaena_marginata"),
(10, "Bamboo Palm", "Chamaedorea seifrizii", "Moderate", "Low to bright", "1.5 m", "Green", "Moderate", "Keep soil moist", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Chamaedorea_seifrizii.jpg/320px-Chamaedorea_seifrizii.jpg", "https://en.wikipedia.org/wiki/Chamaedorea_seifrizii"),
(11, "Monstera", "Monstera deliciosa", "Moderate", "Indirect light", "Up to 3 m", "Green", "Fast", "Water when soil is dry", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Monstera_deliciosa_%28fruit%29.jpg/320px-Monstera_deliciosa_%28fruit%29.jpg", "https://en.wikipedia.org/wiki/Monstera_deliciosa"),
(12, "Spiderwort", "Tradescantia", "Moderate", "Indirect light", "30 cm", "Purple", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Tradescantia_pallida.jpg/320px-Tradescantia_pallida.jpg", "https://en.wikipedia.org/wiki/Tradescantia"),
(13, "Crown of Thorns", "Euphorbia milii", "Low", "Bright", "Up to 1 m", "Red/Pink", "Moderate", "Water when soil is dry", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Euphorbia_milii_01.jpg/320px-Euphorbia_milii_01.jpg", "https://en.wikipedia.org/wiki/Euphorbia_milii"),
(14, "Coleus", "Solenostemon", "Moderate", "Indirect light", "30 cm", "Various", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Coleus_blumei.jpg/320px-Coleus_blumei.jpg", "https://en.wikipedia.org/wiki/Coleus"),
(15, "Fuchsia", "Fuchsia spp.", "Moderate", "Partial sun", "Up to 1 m", "Pink/Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Fuchsia.jpg/320px-Fuchsia.jpg", "https://en.wikipedia.org/wiki/Fuchsia"),
(16, "Amaryllis", "Hippeastrum", "Moderate", "Bright", "Up to 60 cm", "Red/White", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Hippeastrum_sp._flower.jpg/320px-Hippeastrum_sp._flower.jpg", "https://en.wikipedia.org/wiki/Hippeastrum"),
(17, "Petunia", "Petunia spp.", "High", "Full sun", "30 cm", "Various", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Petunia_pulverulenta.jpg/320px-Petunia_pulverulenta.jpg", "https://en.wikipedia.org/wiki/Petunia"),
(18, "Geranium", "Pelargonium", "Moderate", "Full sun", "60 cm", "Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Pelargonium_graveolens.jpg/320px-Pelargonium_graveolens.jpg", "https://en.wikipedia.org/wiki/Geranium"),
(19, "Sweet Pea", "Lathyrus odoratus", "Moderate", "Full sun", "Up to 2 m", "Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Lathyrus_odoratus.jpg/320px-Lathyrus_odoratus.jpg", "https://en.wikipedia.org/wiki/Sweet_pea"),
(20, "Cress", "Lepidium sativum", "High", "Full sun", "30 cm", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Lepidium_sativum.jpg/320px-Lepidium_sativum.jpg", "https://en.wikipedia.org/wiki/Lepidium_sativum"),
(21, "Chamomile", "Matricaria chamomilla", "Moderate", "Full sun", "30 cm", "White", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Matricaria_chamomilla.jpg/320px-Matricaria_chamomilla.jpg", "https://en.wikipedia.org/wiki/Matricaria_chamomilla"),
(22, "Pansy", "Viola tricolor var. hortensis", "Moderate", "Full sun", "30 cm", "Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Pansy_1.jpg/320px-Pansy_1.jpg", "https://en.wikipedia.org/wiki/Pansy"),
(23, "Bleeding Heart", "Dicentra spectabilis", "Moderate", "Partial sun", "Up to 1 m", "Pink", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Dicentra_spectabilis.jpg/320px-Dicentra_spectabilis.jpg", "https://en.wikipedia.org/wiki/Dicentra_spectabilis"),
(24, "Foxglove", "Digitalis purpurea", "Moderate", "Full sun", "1.5 m", "Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Digitalis_purpurea_%28flower%29.jpg/320px-Digitalis_purpurea_%28flower%29.jpg", "https://en.wikipedia.org/wiki/Digitalis_purpurea"),
(25, "Primrose", "Primula vulgaris", "Moderate", "Partial sun", "Up to 30 cm", "Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Primula_vulgaris.jpg/320px-Primula_vulgaris.jpg", "https://en.wikipedia.org/wiki/Primula_vulgaris"),
(26, "Hibiscus", "Hibiscus rosa-sinensis", "High", "Full sun", "Up to 2 m", "Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Hibiscus_rosa-sinensis.jpg/320px-Hibiscus_rosa-sinensis.jpg", "https://en.wikipedia.org/wiki/Hibiscus_rosa-sinensis"),
(27, "Lavender", "Lavandula angustifolia", "High", "Full sun", "Up to 1 m", "Purple", "Slow", "Water when dry", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Lavandula_angustifolia%2C_2015-06-04%2C_Ger.jpg/320px-Lavandula_angustifolia%2C_2015-06-04%2C_Ger.jpg", "https://en.wikipedia.org/wiki/Lavandula_angustifolia"),
(28, "Zinnia", "Zinnia elegans", "High", "Full sun", "Up to 1 m", "Various", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Zinnia_elegans_1.jpg/320px-Zinnia_elegans_1.jpg", "https://en.wikipedia.org/wiki/Zinnia_elegans"),
(29, "Chrysanthemum", "Chrysanthemum morifolium", "Moderate", "Full sun", "Up to 90 cm", "Various", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Chrysanthemum_morifolium.jpg/320px-Chrysanthemum_morifolium.jpg", "https://en.wikipedia.org/wiki/Chrysanthemum"),
(30, "Beggonia", "Begonia spp.", "Moderate", "Indirect light", "Up to 60 cm", "Various", "Moderate", "Water when dry", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Begonia_aleanensis.jpg/320px-Begonia_aleanensis.jpg", "https://en.wikipedia.org/wiki/Begonia"),
(31, "Gerbera Daisy", "Gerbera jamesonii", "High", "Full sun", "Up to 60 cm", "Various", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Gerbera_jamesonii.jpg/320px-Gerbera_jamesonii.jpg", "https://en.wikipedia.org/wiki/Gerbera_jamesonii"),
(32, "Kalanchoe", "Kalanchoe blossfeldiana", "High", "Bright, indirect", "Up to 30 cm", "Various", "Moderate", "Water when soil is dry", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Kalanchoe_blossfeldiana_001.jpg/320px-Kalanchoe_blossfeldiana_001.jpg", "https://en.wikipedia.org/wiki/Kalanchoe_blossfeldiana"),
(33, "African Violet", "Saintpaulia", "Moderate", "Indirect light", "Up to 30 cm", "Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Saintpaulia_rif_7.jpg/320px-Saintpaulia_rif_7.jpg", "https://en.wikipedia.org/wiki/Saintpaulia"),
(34, "Basil", "Ocimum basilicum", "High", "Full sun", "Up to 60 cm", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Ocimum_basilicum_002.jpg/320px-Ocimum_basilicum_002.jpg", "https://en.wikipedia.org/wiki/Basil"),
(35, "Mint", "Mentha", "Moderate", "Full sun", "Up to 90 cm", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Mentha_spicata.jpg/320px-Mentha_spicata.jpg", "https://en.wikipedia.org/wiki/Mint"),
(36, "Thyme", "Thymus vulgaris", "High", "Full sun", "Up to 30 cm", "Green", "Slow", "Water when soil is dry", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Thymus_vulgaris.jpg/320px-Thymus_vulgaris.jpg", "https://en.wikipedia.org/wiki/Thyme"),
(37, "Oregano", "Origanum vulgare", "High", "Full sun", "Up to 30 cm", "Green", "Moderate", "Water when soil is dry", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Origanum_vulgare.jpg/320px-Origanum_vulgare.jpg", "https://en.wikipedia.org/wiki/Oregano"),
(38, "Rosemary", "Salvia rosmarinus", "High", "Full sun", "Up to 1 m", "Green", "Slow", "Water when soil is dry", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Rosmarinus_officinalis.jpg/320px-Rosmarinus_officinalis.jpg", "https://en.wikipedia.org/wiki/Rosemary"),
(39, "Chives", "Allium schoenoprasum", "High", "Full sun", "Up to 30 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Allium_schoenoprasum_001.jpg/320px-Allium_schoenoprasum_001.jpg", "https://en.wikipedia.org/wiki/Chives"),
(40, "Sage", "Salvia officinalis", "High", "Full sun", "Up to 60 cm", "Green", "Slow", "Water when soil is dry", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Salvia_officinalis.jpg/320px-Salvia_officinalis.jpg", "https://en.wikipedia.org/wiki/Sage"),
(41, "Tomato", "Solanum lycopersicum", "High", "Full sun", "Up to 1.5 m", "Red", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Solanum_lycopersicum_3.jpg/320px-Solanum_lycopersicum_3.jpg", "https://en.wikipedia.org/wiki/Tomato"),
(42, "Cucumber", "Cucumis sativus", "High", "Full sun", "Up to 2 m", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Cucumis_sativus.jpg/320px-Cucumis_sativus.jpg", "https://en.wikipedia.org/wiki/Cucumber"),
(43, "Lettuce", "Lactuca sativa", "Moderate", "Full sun", "Up to 30 cm", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Lactuca_sativa_lettuce.jpg/320px-Lactuca_sativa_lettuce.jpg", "https://en.wikipedia.org/wiki/Lettuce"),
(44, "Carrot", "Daucus carota", "Moderate", "Full sun", "Up to 30 cm", "Orange", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Daucus_carota_%28carrot%29.jpg/320px-Daucus_carota_%28carrot%29.jpg", "https://en.wikipedia.org/wiki/Carrot"),
(45, "Radish", "Raphanus sativus", "High", "Full sun", "Up to 30 cm", "Red", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Raphanus_sativus_%28radish%29.jpg/320px-Raphanus_sativus_%28radish%29.jpg", "https://en.wikipedia.org/wiki/Radish"),
(46, "Bean", "Phaseolus vulgaris", "High", "Full sun", "Up to 3 m", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Phaseolus_vulgaris.jpg/320px-Phaseolus_vulgaris.jpg", "https://en.wikipedia.org/wiki/Bean"),
(47, "Pea", "Pisum sativum", "High", "Full sun", "Up to 1.5 m", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Pisum_sativum.jpg/320px-Pisum_sativum.jpg", "https://en.wikipedia.org/wiki/Pea"),
(48, "Strawberry", "Fragaria × ananassa", "High", "Full sun", "Up to 30 cm", "Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Strawberry_plant_%28fruits%29.jpg/320px-Strawberry_plant_%28fruits%29.jpg", "https://en.wikipedia.org/wiki/Strawberry"),
(49, "Blueberry", "Vaccinium corymbosum", "Moderate", "Full sun", "Up to 1.5 m", "Blue", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Blueberry_mature_fruit.jpg/320px-Blueberry_mature_fruit.jpg", "https://en.wikipedia.org/wiki/Blueberry"),
(50, "Blackberry", "Rubus fruticosus", "Moderate", "Full sun", "Up to 1.5 m", "Black", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Blackberry.jpg/320px-Blackberry.jpg", "https://en.wikipedia.org/wiki/Blackberry"),
(51, "Raspberry", "Rubus idaeus", "Moderate", "Full sun", "Up to 1.5 m", "Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Raspberry_%28Rubus_idaeus%29.jpg/320px-Raspberry_%28Rubus_idaeus%29.jpg", "https://en.wikipedia.org/wiki/Raspberry"),
(52, "Apple", "Malus domestica", "High", "Full sun", "Up to 3 m", "Red", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Malus_domestica_002.jpg/320px-Malus_domestica_002.jpg", "https://en.wikipedia.org/wiki/Malus_domestica"),
(53, "Pear", "Pyrus", "Moderate", "Full sun", "Up to 3 m", "Green", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Pyrus_cordata.jpg/320px-Pyrus_cordata.jpg", "https://en.wikipedia.org/wiki/Pear"),
(54, "Peach", "Prunus persica", "Moderate", "Full sun", "Up to 3 m", "Peach", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Prunus_persica_001.jpg/320px-Prunus_persica_001.jpg", "https://en.wikipedia.org/wiki/Peach"),
(55, "Plum", "Prunus domestica", "Moderate", "Full sun", "Up to 3 m", "Purple", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Prunus_domestica_plum.jpg/320px-Prunus_domestica_plum.jpg", "https://en.wikipedia.org/wiki/Plum"),
(56, "Cherry", "Prunus avium", "Moderate", "Full sun", "Up to 3 m", "Red", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Cherry_Stella-Deluxe.jpg/320px-Cherry_Stella-Deluxe.jpg", "https://en.wikipedia.org/wiki/Cherry"),
(57, "Grape", "Vitis vinifera", "High", "Full sun", "Up to 3 m", "Purple", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Vitis_vinifera_grape_bunch.jpg/320px-Vitis_vinifera_grape_bunch.jpg", "https://en.wikipedia.org/wiki/Vitis_vinifera"),
(58, "Watermelon", "Citrullus lanatus", "High", "Full sun", "Up to 3 m", "Green/Red", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Watermelon02.jpg/320px-Watermelon02.jpg", "https://en.wikipedia.org/wiki/Watermelon"),
(59, "Cantaloupe", "Cucumis melo", "High", "Full sun", "Up to 1.5 m", "Orange", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Cantaloupe.JPG/320px-Cantaloupe.JPG", "https://en.wikipedia.org/wiki/Cantaloupe"),
(60, "Honeydew", "Cucumis melo", "High", "Full sun", "Up to 1.5 m", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Honeydew.jpg/320px-Honeydew.jpg", "https://en.wikipedia.org/wiki/Honeydew"),
(61, "Pumpkin", "Cucurbita pepo", "High", "Full sun", "Up to 3 m", "Orange", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Cucurbita_pepo_1.jpg/320px-Cucurbita_pepo_1.jpg", "https://en.wikipedia.org/wiki/Pumpkin"),
(62, "Squash", "Cucurbita spp.", "High", "Full sun", "Up to 2 m", "Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Cucurbita_maxima_1.jpg/320px-Cucurbita_maxima_1.jpg", "https://en.wikipedia.org/wiki/Squash_(plant)"),
(63, "Zucchini", "Cucurbita pepo", "High", "Full sun", "Up to 1 m", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Zucchini.jpg/320px-Zucchini.jpg", "https://en.wikipedia.org/wiki/Zucchini"),
(64, "Eggplant", "Solanum melongena", "High", "Full sun", "Up to 1.5 m", "Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Solanum_melongena.jpg/320px-Solanum_melongena.jpg", "https://en.wikipedia.org/wiki/Eggplant"),
(65, "Artichoke", "Cynara cardunculus", "High", "Full sun", "Up to 1.5 m", "Purple", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Cynara_cardunculus.jpg/320px-Cynara_cardunculus.jpg", "https://en.wikipedia.org/wiki/Artichoke"),
(66, "Lettuce", "Lactuca sativa", "High", "Full sun", "30 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Lettuce.jpg/320px-Lettuce.jpg", "https://en.wikipedia.org/wiki/Lettuce"),
(67, "Cabbage", "Brassica oleracea", "Moderate", "Full sun", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Brassica_oleracea.jpg/320px-Brassica_oleracea.jpg", "https://en.wikipedia.org/wiki/Cabbage"),
(68, "Cauliflower", "Brassica oleracea var. botrytis", "Moderate", "Full sun", "Up to 1 m", "White", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/White_Cauliflower.jpg/320px-White_Cauliflower.jpg", "https://en.wikipedia.org/wiki/Cauliflower"),
(69, "Broccoli", "Brassica oleracea var. italica", "Moderate", "Full sun", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Broccoli.jpg/320px-Broccoli.jpg", "https://en.wikipedia.org/wiki/Broccoli"),
(70, "Kale", "Brassica oleracea var. sabellica", "Moderate", "Full sun", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Kale.JPG/320px-Kale.JPG", "https://en.wikipedia.org/wiki/Kale"),
(71, "Spinach", "Spinacia oleracea", "High", "Full sun", "Up to 30 cm", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Spinach_%28Spinacia_oleracea%29.jpg/320px-Spinach_%28Spinacia_oleracea%29.jpg", "https://en.wikipedia.org/wiki/Spinach"),
(72, "Arugula", "Eruca vesicaria", "High", "Full sun", "Up to 30 cm", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Eruca_vesicaria.jpg/320px-Eruca_vesicaria.jpg", "https://en.wikipedia.org/wiki/Arugula"),
(73, "Mustard", "Brassica juncea", "High", "Full sun", "Up to 1 m", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Brassica_juncea.jpg/320px-Brassica_juncea.jpg", "https://en.wikipedia.org/wiki/Mustard_(plant)"),
(74, "Bok Choy", "Brassica rapa", "Moderate", "Full sun", "Up to 60 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Bok_Choy.jpg/320px-Bok_Choy.jpg", "https://en.wikipedia.org/wiki/Bok_choy"),
(75, "Fennel", "Foeniculum vulgare", "High", "Full sun", "Up to 1.5 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Foeniculum_vulgare_%28flowering%29.jpg/320px-Foeniculum_vulgare_%28flowering%29.jpg", "https://en.wikipedia.org/wiki/Fennel"),
(76, "Carrot", "Daucus carota", "Moderate", "Full sun", "Up to 30 cm", "Orange", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Daucus_carota.jpg/320px-Daucus_carota.jpg", "https://en.wikipedia.org/wiki/Carrot"),
(77, "Turnip", "Brassica rapa", "Moderate", "Full sun", "Up to 30 cm", "Purple/White", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Turnip.jpg/320px-Turnip.jpg", "https://en.wikipedia.org/wiki/Turnip"),
(78, "Beetroot", "Beta vulgaris", "Moderate", "Full sun", "Up to 1 m", "Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Beetroot_%28Beta_vulgaris%29.jpg/320px-Beetroot_%28Beta_vulgaris%29.jpg", "https://en.wikipedia.org/wiki/Beetroot"),
(79, "Leek", "Allium ampeloprasum", "High", "Full sun", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Leeks_Farm_Fresh.jpg/320px-Leeks_Farm_Fresh.jpg", "https://en.wikipedia.org/wiki/Leek"),
(80, "Onion", "Allium cepa", "High", "Full sun", "Up to 1 m", "Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Allium_cepa.jpg/320px-Allium_cepa.jpg", "https://en.wikipedia.org/wiki/Onion"),
(81, "Garlic", "Allium sativum", "High", "Full sun", "Up to 60 cm", "White", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Garlic.jpg/320px-Garlic.jpg", "https://en.wikipedia.org/wiki/Garlic"),
(82, "Chili Pepper", "Capsicum annuum", "High", "Full sun", "Up to 1.5 m", "Red/Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Capsicum_annuum_1.jpg/320px-Capsicum_annuum_1.jpg", "https://en.wikipedia.org/wiki/Chili_pepper"),
(83, "Bell Pepper", "Capsicum annuum", "High", "Full sun", "Up to 1.5 m", "Green/Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Bell_pepper.jpg/320px-Bell_pepper.jpg", "https://en.wikipedia.org/wiki/Bell_pepper"),
(84, "Sweet Potato", "Ipomoea batatas", "High", "Full sun", "Up to 1 m", "Orange", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Sweet_Potato_01.jpg/320px-Sweet_Potato_01.jpg", "https://en.wikipedia.org/wiki/Sweet_potato"),
(85, "Potato", "Solanum tuberosum", "High", "Full sun", "Up to 1 m", "Brown", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Potato_plant.jpg/320px-Potato_plant.jpg", "https://en.wikipedia.org/wiki/Potato"),
(86, "Yam", "Dioscorea spp.", "High", "Full sun", "Up to 1 m", "Purple/Brown", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Dioscorea_bulbifera_%28yam%29.jpg/320px-Dioscorea_bulbifera_%28yam%29.jpg", "https://en.wikipedia.org/wiki/Yam"),
(87, "Cucumber", "Cucumis sativus", "High", "Full sun", "Up to 2 m", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Cucumis_sativus.jpg/320px-Cucumis_sativus.jpg", "https://en.wikipedia.org/wiki/Cucumber"),
(88, "Melon", "Cucumis melo", "High", "Full sun", "Up to 1.5 m", "Yellow/Orange", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Cucumis_melo_%28melon%29.jpg/320px-Cucumis_melo_%28melon%29.jpg", "https://en.wikipedia.org/wiki/Melon"),
(89, "Tomato", "Solanum lycopersicum", "High", "Full sun", "Up to 1.5 m", "Red", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Solanum_lycopersicum.jpg/320px-Solanum_lycopersicum.jpg", "https://en.wikipedia.org/wiki/Tomato"),
(90, "Cabbage", "Brassica oleracea", "Moderate", "Full sun", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Brassica_oleracea.jpg/320px-Brassica_oleracea.jpg", "https://en.wikipedia.org/wiki/Cabbage"),
(91, "Chard", "Beta vulgaris var. cicla", "Moderate", "Full sun", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Swiss_chard_plant.jpg/320px-Swiss_chard_plant.jpg", "https://en.wikipedia.org/wiki/Chard"),
(92, "Collard Greens", "Brassica oleracea var. viridis", "Moderate", "Full sun", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Collard_greens_plant.jpg/320px-Collard_greens_plant.jpg", "https://en.wikipedia.org/wiki/Collard_greens"),
(93, "Chicory", "Cichorium intybus", "Moderate", "Full sun", "Up to 1.5 m", "Blue", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Cichorium_intybus_3.jpg/320px-Cichorium_intybus_3.jpg", "https://en.wikipedia.org/wiki/Chicory"),
(94, "Endive", "Cichorium endivia", "Moderate", "Full sun", "Up to 60 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Endive.jpg/320px-Endive.jpg", "https://en.wikipedia.org/wiki/Endive"),
(95, "Mache", "Valerianella locusta", "High", "Full sun", "Up to 30 cm", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Mache_%28Valerianella_locusta%29.jpg/320px-Mache_%28Valerianella_locusta%29.jpg", "https://en.wikipedia.org/wiki/Mache"),
(96, "Radicchio", "Cichorium intybus", "Moderate", "Full sun", "Up to 30 cm", "Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Radicchio.jpg/320px-Radicchio.jpg", "https://en.wikipedia.org/wiki/Radicchio"),
(97, "Okra", "Abelmoschus esculentus", "High", "Full sun", "Up to 1.5 m", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Okra_%28Abelmoschus_esculentus%29.jpg/320px-Okra_%28Abelmoschus_esculentus%29.jpg", "https://en.wikipedia.org/wiki/Okra"),
(98, "Chard", "Beta vulgaris", "Moderate", "Full sun", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Swiss_chard_plant.jpg/320px-Swiss_chard_plant.jpg", "https://en.wikipedia.org/wiki/Chard"),
(99, "Kohlrabi", "Brassica oleracea", "Moderate", "Full sun", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Kohlrabi.jpg/320px-Kohlrabi.jpg", "https://en.wikipedia.org/wiki/Kohlrabi"),
(100, "Rutabaga", "Brassica napus", "Moderate", "Full sun", "Up to 1 m", "Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Rutabaga.jpg/320px-Rutabaga.jpg", "https://en.wikipedia.org/wiki/Rutabaga"),
(101, "Acer", "Aceraceae", "Moderate", "Full sun", "Up to 20 m", "Green/Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Acer_palmatum_leaves_autumn.jpg/320px-Acer_palmatum_leaves_autumn.jpg", "https://en.wikipedia.org/wiki/Acer"),
(102, "Aloe Vera", "Aloe barbadensis miller", "Low", "Bright, indirect", "30 cm", "Yellow", "Slow", "Water when dry", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Aloe_vera_flower2.jpg/320px-Aloe_vera_flower2.jpg", "https://en.wikipedia.org/wiki/Aloe_vera"),
(103, "Echinacea", "Echinacea purpurea", "Moderate", "Full sun", "Up to 1.2 m", "Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Echinacea_purpurea_2.jpg/320px-Echinacea_purpurea_2.jpg", "https://en.wikipedia.org/wiki/Echinacea"),
(104, "Lobelia", "Lobelia erinus", "Low", "Full sun", "30 cm", "Blue", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Lobelia_erinus.jpg/320px-Lobelia_erinus.jpg", "https://en.wikipedia.org/wiki/Lobelia"),
(105, "Verbena", "Verbena spp.", "Low", "Full sun", "Up to 1 m", "Various", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Verbena.jpg/320px-Verbena.jpg", "https://en.wikipedia.org/wiki/Verbena"),
(106, "Snapdragon", "Antirrhinum majus", "Moderate", "Full sun", "Up to 90 cm", "Various", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Snapdragon_Flower.jpg/320px-Snapdragon_Flower.jpg", "https://en.wikipedia.org/wiki/Snapdragon"),
(107, "Zinnia", "Zinnia elegans", "High", "Full sun", "Up to 1 m", "Various", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Zinnia_elegans_flower.jpg/320px-Zinnia_elegans_flower.jpg", "https://en.wikipedia.org/wiki/Zinnia"),
(108, "Marigold", "Tagetes", "High", "Full sun", "Up to 60 cm", "Yellow/Orange", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Tagetes_erecta.jpg/320px-Tagetes_erecta.jpg", "https://en.wikipedia.org/wiki/Marigold"),
(109, "Calendula", "Calendula officinalis", "Moderate", "Full sun", "Up to 50 cm", "Orange", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Calendula_officinalis_2005.jpg/320px-Calendula_officinalis_2005.jpg", "https://en.wikipedia.org/wiki/Calendula"),
(110, "Chrysanthemum", "Chrysanthemum morifolium", "High", "Full sun", "Up to 1 m", "Various", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Chrysanthemum_in_full_bloom.jpg/320px-Chrysanthemum_in_full_bloom.jpg", "https://en.wikipedia.org/wiki/Chrysanthemum"),
(111, "Fuchsia", "Fuchsia spp.", "Moderate", "Partial shade", "Up to 1 m", "Pink/Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Fuchsia.jpg/320px-Fuchsia.jpg", "https://en.wikipedia.org/wiki/Fuchsia"),
(112, "Tuberose", "Polianthes tuberosa", "Moderate", "Full sun", "Up to 1.2 m", "White", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Polianthes_tuberosa.jpg/320px-Polianthes_tuberosa.jpg", "https://en.wikipedia.org/wiki/Tuberose"),
(113, "Peony", "Paeonia", "Moderate", "Full sun", "Up to 1 m", "Various", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Paeonia_rosea.jpg/320px-Paeonia_rosea.jpg", "https://en.wikipedia.org/wiki/Peony"),
(114, "Camellia", "Camellia japonica", "Moderate", "Partial shade", "Up to 4 m", "Pink/White/Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Camellia_japonica_var._tricolor.jpg/320px-Camellia_japonica_var._tricolor.jpg", "https://en.wikipedia.org/wiki/Camellia"),
(115, "Daffodil", "Narcissus", "High", "Full sun", "Up to 30 cm", "Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Narcissus_pseudonarcissus.JPG/320px-Narcissus_pseudonarcissus.JPG", "https://en.wikipedia.org/wiki/Daffodil"),
(116, "Tulip", "Tulipa", "High", "Full sun", "Up to 30 cm", "Various", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Tulip.JPG/320px-Tulip.JPG", "https://en.wikipedia.org/wiki/Tulip"),
(117, "Crocus", "Crocus sativus", "Moderate", "Full sun", "Up to 20 cm", "Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Crocus_sativus_1.jpg/320px-Crocus_sativus_1.jpg", "https://en.wikipedia.org/wiki/Crocus"),
(118, "Hyacinth", "Hyacinthus orientalis", "High", "Full sun", "Up to 30 cm", "Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Hyacinthus_orientalis_2013.jpg/320px-Hyacinthus_orientalis_2013.jpg", "https://en.wikipedia.org/wiki/Hyacinth"),
(119, "Iris", "Iris germanica", "Moderate", "Full sun", "Up to 1 m", "Various", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Iris_germanica_flowers.jpg/320px-Iris_germanica_flowers.jpg", "https://en.wikipedia.org/wiki/Iris"),
(120, "Freesia", "Freesia refracta", "Moderate", "Full sun", "Up to 50 cm", "Various", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Freesia.JPG/320px-Freesia.JPG", "https://en.wikipedia.org/wiki/Freesia"),
(121, "Calla Lily", "Zantedeschia", "Moderate", "Full sun", "Up to 1 m", "White", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Calla_Lily_in_full_bloom.jpg/320px-Calla_Lily_in_full_bloom.jpg", "https://en.wikipedia.org/wiki/Calla_lily"),
(122, "Fennel", "Foeniculum vulgare", "Moderate", "Full sun", "Up to 2 m", "Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Foeniculum_vulgare.jpg/320px-Foeniculum_vulgare.jpg", "https://en.wikipedia.org/wiki/Fennel"),
(123, "Kale", "Brassica oleracea", "High", "Full sun", "Up to 60 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Kale_plant.jpg/320px-Kale_plant.jpg", "https://en.wikipedia.org/wiki/Kale"),
(124, "Carrot", "Daucus carota", "High", "Full sun", "Up to 30 cm", "Orange", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Carrot.jpg/320px-Carrot.jpg", "https://en.wikipedia.org/wiki/Carrot"),
(125, "Lettuce", "Lactuca sativa", "High", "Full sun", "Up to 30 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Lactuca_sativa.jpg/320px-Lactuca_sativa.jpg", "https://en.wikipedia.org/wiki/Lettuce"),
(126, "Spinach", "Spinacia oleracea", "High", "Full sun", "Up to 30 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Spinacia_oleracea_plant.jpg/320px-Spinacia_oleracea_plant.jpg", "https://en.wikipedia.org/wiki/Spinach"),
(127, "Radish", "Raphanus sativus", "High", "Full sun", "Up to 30 cm", "Red/White", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Raphanus_sativus.jpg/320px-Raphanus_sativus.jpg", "https://en.wikipedia.org/wiki/Radish"),
(128, "Leek", "Allium ampeloprasum", "Moderate", "Full sun", "Up to 60 cm", "White/Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Leeks_in_the_garden.jpg/320px-Leeks_in_the_garden.jpg", "https://en.wikipedia.org/wiki/Leek"),
(129, "Onion", "Allium cepa", "High", "Full sun", "Up to 1 m", "White/Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Onion_plant.jpg/320px-Onion_plant.jpg", "https://en.wikipedia.org/wiki/Onion"),
(130, "Garlic", "Allium sativum", "Moderate", "Full sun", "Up to 60 cm", "White", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Garlic_plant.jpg/320px-Garlic_plant.jpg", "https://en.wikipedia.org/wiki/Garlic"),
(131, "Chili Pepper", "Capsicum", "High", "Full sun", "Up to 1 m", "Red/Yellow/Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Chili_peppers.jpg/320px-Chili_peppers.jpg", "https://en.wikipedia.org/wiki/Chili_pepper"),
(132, "Sweet Corn", "Zea mays", "High", "Full sun", "Up to 2.5 m", "Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Sweetcorn_in_bloom.jpg/320px-Sweetcorn_in_bloom.jpg", "https://en.wikipedia.org/wiki/Sweetcorn"),
(133, "Okra", "Abelmoschus esculentus", "High", "Full sun", "Up to 1.5 m", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Okra_%28Abelmoschus_esculentus%29.jpg/320px-Okra_%28Abelmoschus_esculentus%29.jpg", "https://en.wikipedia.org/wiki/Okra"),
(134, "Broccoli", "Brassica oleracea", "High", "Full sun", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Broccoli_plant.jpg/320px-Broccoli_plant.jpg", "https://en.wikipedia.org/wiki/Broccoli"),
(135, "Cauliflower", "Brassica oleracea", "High", "Full sun", "Up to 1 m", "White", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Cauliflower.jpg/320px-Cauliflower.jpg", "https://en.wikipedia.org/wiki/Cauliflower"),
(136, "Cabbage", "Brassica oleracea", "High", "Full sun", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Cabbage_plant.jpg/320px-Cabbage_plant.jpg", "https://en.wikipedia.org/wiki/Cabbage"),
(137, "Asparagus", "Asparagus officinalis", "Moderate", "Full sun", "Up to 1.5 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Asparagus_officinalis_plant.jpg/320px-Asparagus_officinalis_plant.jpg", "https://en.wikipedia.org/wiki/Asparagus"),
(138, "Rhubarb", "Rheum rhabarbarum", "Moderate", "Full sun", "Up to 1.5 m", "Red", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Rhubarb_leaves.jpg/320px-Rhubarb_leaves.jpg", "https://en.wikipedia.org/wiki/Rhubarb"),
(139, "Pumpkin", "Cucurbita pepo", "High", "Full sun", "Up to 3 m", "Orange", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Pumpkin_growing_on_vine.jpg/320px-Pumpkin_growing_on_vine.jpg", "https://en.wikipedia.org/wiki/Pumpkin"),
(140, "Squash", "Cucurbita", "High", "Full sun", "Up to 2 m", "Yellow/Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Squash_growing_in_garden.jpg/320px-Squash_growing_in_garden.jpg", "https://en.wikipedia.org/wiki/Squash_(plant)"),
(141, "Tomato", "Solanum lycopersicum", "High", "Full sun", "Up to 1.5 m", "Red/Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Tomato_2013_G1.jpg/320px-Tomato_2013_G1.jpg", "https://en.wikipedia.org/wiki/Tomato"),
(142, "Cucumber", "Cucumis sativus", "High", "Full sun", "Up to 2 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Cucumber_4.jpg/320px-Cucumber_4.jpg", "https://en.wikipedia.org/wiki/Cucumber"),
(143, "Pea", "Pisum sativum", "High", "Full sun", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Peas.jpg/320px-Peas.jpg", "https://en.wikipedia.org/wiki/Pea"),
(144, "Sweet Potato", "Ipomoea batatas", "High", "Full sun", "Up to 1.5 m", "Orange", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Sweet_potato_plants.jpg/320px-Sweet_potato_plants.jpg", "https://en.wikipedia.org/wiki/Sweet_potato"),
(145, "Watermelon", "Citrullus lanatus", "High", "Full sun", "Up to 2 m", "Green/Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Watermelon_3.jpg/320px-Watermelon_3.jpg", "https://en.wikipedia.org/wiki/Watermelon"),
(146, "Melon", "Cucumis melo", "High", "Full sun", "Up to 1.5 m", "Green/Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Cantaloupe_Whole_and_Sliced.jpg/320px-Cantaloupe_Whole_and_Sliced.jpg", "https://en.wikipedia.org/wiki/Melon"),
(147, "Bell Pepper", "Capsicum annuum", "High", "Full sun", "Up to 1 m", "Red/Yellow/Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Bell_pepper.jpg/320px-Bell_pepper.jpg", "https://en.wikipedia.org/wiki/Bell_pepper"),
(148, "Eggplant", "Solanum melongena", "High", "Full sun", "Up to 1 m", "Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Eggplant_Orlando.jpg/320px-Eggplant_Orlando.jpg", "https://en.wikipedia.org/wiki/Eggplant"),
(149, "Zucchini", "Cucurbita pepo", "High", "Full sun", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Zucchini.jpg/320px-Zucchini.jpg", "https://en.wikipedia.org/wiki/Zucchini"),
(150, "Radicchio", "Cichorium intybus", "High", "Full sun", "Up to 30 cm", "Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Radicchio_2006.jpg/320px-Radicchio_2006.jpg", "https://en.wikipedia.org/wiki/Radicchio"),
(151, "Arugula", "Eruca vesicaria", "High", "Full sun", "Up to 30 cm", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Arugula_plant.jpg/320px-Arugula_plant.jpg", "https://en.wikipedia.org/wiki/Arugula"),
(152, "Basil", "Ocimum basilicum", "High", "Full sun", "Up to 60 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Basil_plant.jpg/320px-Basil_plant.jpg", "https://en.wikipedia.org/wiki/Basil"),
(153, "Oregano", "Origanum vulgare", "High", "Full sun", "Up to 60 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Oregano_plant.jpg/320px-Oregano_plant.jpg", "https://en.wikipedia.org/wiki/Oregano"),
(154, "Mint", "Mentha", "High", "Full sun", "Up to 90 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Mint_leaves.jpg/320px-Mint_leaves.jpg", "https://en.wikipedia.org/wiki/Mint"),
(155, "Rosemary", "Salvia rosmarinus", "High", "Full sun", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Rosemary_plant.jpg/320px-Rosemary_plant.jpg", "https://en.wikipedia.org/wiki/Rosemary"),
(156, "Thyme", "Thymus vulgaris", "High", "Full sun", "Up to 30 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Thyme.jpg/320px-Thyme.jpg", "https://en.wikipedia.org/wiki/Thyme"),
(157, "Sage", "Salvia officinalis", "High", "Full sun", "Up to 90 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Sage_plant.jpg/320px-Sage_plant.jpg", "https://en.wikipedia.org/wiki/Sage"),
(158, "Lavender", "Lavandula angustifolia", "High", "Full sun", "Up to 1 m", "Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Lavender_in_full_bloom.jpg/320px-Lavender_in_full_bloom.jpg", "https://en.wikipedia.org/wiki/Lavender"),
(159, "Chives", "Allium schoenoprasum", "High", "Full sun", "Up to 30 cm", "Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Chives.JPG/320px-Chives.JPG", "https://en.wikipedia.org/wiki/Chives"),
(160, "Dill", "Anethum graveolens", "High", "Full sun", "Up to 1 m", "Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Dill_plant.jpg/320px-Dill_plant.jpg", "https://en.wikipedia.org/wiki/Dill"),
(161, "Cilantro", "Coriandrum sativum", "High", "Full sun", "Up to 60 cm", "White", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Coriander.jpg/320px-Coriander.jpg", "https://en.wikipedia.org/wiki/Coriander"),
(162, "Fennel", "Foeniculum vulgare", "Moderate", "Full sun", "Up to 2 m", "Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Foeniculum_vulgare.jpg/320px-Foeniculum_vulgare.jpg", "https://en.wikipedia.org/wiki/Fennel"),
(163, "Chard", "Beta vulgaris", "High", "Full sun", "Up to 60 cm", "Green/Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Swiss_chard.jpg/320px-Swiss_chard.jpg", "https://en.wikipedia.org/wiki/Chard"),
(164, "Kohlrabi", "Brassica oleracea", "High", "Full sun", "Up to 60 cm", "Green/Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Kohlrabi.jpg/320px-Kohlrabi.jpg", "https://en.wikipedia.org/wiki/Kohlrabi"),
(165, "Mustard Greens", "Brassica juncea", "High", "Full sun", "Up to 60 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Mustard_Greens.jpg/320px-Mustard_Greens.jpg", "https://en.wikipedia.org/wiki/Mustard_greens"),
(166, "Bok Choy", "Brassica rapa", "High", "Full sun", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Bok_Choy.jpg/320px-Bok_Choy.jpg", "https://en.wikipedia.org/wiki/Bok_choy"),
(167, "Pak Choi", "Brassica rapa", "High", "Full sun", "Up to 60 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Pak_choi.jpg/320px-Pak_choi.jpg", "https://en.wikipedia.org/wiki/Pak_choi"),
(168, "Chayote", "Sechium edule", "High", "Full sun", "Up to 3 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Chayote_plant.jpg/320px-Chayote_plant.jpg", "https://en.wikipedia.org/wiki/Chayote"),
(169, "Artichoke", "Cynara scolymus", "Moderate", "Full sun", "Up to 2 m", "Purple", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Artichoke_plant.jpg/320px-Artichoke_plant.jpg", "https://en.wikipedia.org/wiki/Artichoke"),
(170, "Endive", "Cichorium endivia", "High", "Full sun", "Up to 30 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Endive.jpg/320px-Endive.jpg", "https://en.wikipedia.org/wiki/Endive"),
(141, "Radicchio", "Cichorium intybus", "High", "Full sun", "Up to 30 cm", "Red/White", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Radicchio.jpg/320px-Radicchio.jpg", "https://en.wikipedia.org/wiki/Radicchio"),
(142, "Celery", "Apium graveolens", "High", "Full sun", "Up to 60 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Celery.jpg/320px-Celery.jpg", "https://en.wikipedia.org/wiki/Celery"),
(143, "Leek", "Allium ampeloprasum", "Moderate", "Full sun", "Up to 60 cm", "White/Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Leeks_in_the_garden.jpg/320px-Leeks_in_the_garden.jpg", "https://en.wikipedia.org/wiki/Leek"),
(144, "Chard", "Beta vulgaris", "High", "Full sun", "Up to 50 cm", "Green/Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Chard.jpg/320px-Chard.jpg", "https://en.wikipedia.org/wiki/Chard"),
(145, "Turnip", "Brassica rapa", "High", "Full sun", "Up to 30 cm", "White/Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Turnip_in_our_garden.jpg/320px-Turnip_in_our_garden.jpg", "https://en.wikipedia.org/wiki/Turnip"),
(146, "Cucumber", "Cucumis sativus", "High", "Full sun", "Up to 2 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Cucumber_2009-1.jpg/320px-Cucumber_2009-1.jpg", "https://en.wikipedia.org/wiki/Cucumber"),
(147, "Tomato", "Solanum lycopersicum", "High", "Full sun", "Up to 2 m", "Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Tomato_je.jpg/320px-Tomato_je.jpg", "https://en.wikipedia.org/wiki/Tomato"),
(148, "Bell Pepper", "Capsicum annuum", "High", "Full sun", "Up to 1 m", "Red/Green/Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Bell_peppers.jpg/320px-Bell_peppers.jpg", "https://en.wikipedia.org/wiki/Bell_pepper"),
(149, "Eggplant", "Solanum melongena", "High", "Full sun", "Up to 1.5 m", "Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eggplant.jpg/320px-Eggplant.jpg", "https://en.wikipedia.org/wiki/Eggplant"),
(150, "Zucchini", "Cucurbita pepo", "High", "Full sun", "Up to 1.5 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Zucchini.jpg/320px-Zucchini.jpg", "https://en.wikipedia.org/wiki/Zucchini"),
(151, "Okra", "Abelmoschus esculentus", "High", "Full sun", "Up to 1.5 m", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Okra_%28Abelmoschus_esculentus%29.jpg/320px-Okra_%28Abelmoschus_esculentus%29.jpg", "https://en.wikipedia.org/wiki/Okra"),
(152, "Sweet Potato", "Ipomoea batatas", "High", "Full sun", "Up to 1 m", "Orange", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Sweet_potato_%28close_up%29.jpg/320px-Sweet_potato_%28close_up%29.jpg", "https://en.wikipedia.org/wiki/Sweet_potato"),
(153, "Potato", "Solanum tuberosum", "High", "Full sun", "Up to 60 cm", "Brown/White", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Potato.jpg/320px-Potato.jpg", "https://en.wikipedia.org/wiki/Potato"),
(154, "Ginger", "Zingiber officinale", "Moderate", "Partial shade", "Up to 1 m", "Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Ginger_plant.jpg/320px-Ginger_plant.jpg", "https://en.wikipedia.org/wiki/Ginger"),
(155, "Turmeric", "Curcuma longa", "Moderate", "Partial shade", "Up to 1 m", "Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Turmeric.jpg/320px-Turmeric.jpg", "https://en.wikipedia.org/wiki/Turmeric"),
(156, "Sage", "Salvia officinalis", "Moderate", "Full sun", "Up to 60 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Sage_plant.jpg/320px-Sage_plant.jpg", "https://en.wikipedia.org/wiki/Sage"),
(157, "Oregano", "Origanum vulgare", "Moderate", "Full sun", "Up to 60 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Oregano_plant.jpg/320px-Oregano_plant.jpg", "https://en.wikipedia.org/wiki/Oregano"),
(158, "Basil", "Ocimum basilicum", "High", "Full sun", "Up to 60 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Basil_leaf_closeup.jpg/320px-Basil_leaf_closeup.jpg", "https://en.wikipedia.org/wiki/Basil"),
(159, "Thyme", "Thymus vulgaris", "Moderate", "Full sun", "Up to 30 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Thyme.jpg/320px-Thyme.jpg", "https://en.wikipedia.org/wiki/Thyme"),
(160, "Parsley", "Petroselinum crispum", "High", "Full sun", "Up to 30 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Parsley.jpg/320px-Parsley.jpg", "https://en.wikipedia.org/wiki/Parsley"),
(161, "Rosemary", "Salvia rosmarinus", "Moderate", "Full sun", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Rosemary_plant.jpg/320px-Rosemary_plant.jpg", "https://en.wikipedia.org/wiki/Rosemary"),
(162, "Mint", "Mentha", "Moderate", "Partial shade", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Mint_plant.jpg/320px-Mint_plant.jpg", "https://en.wikipedia.org/wiki/Mint"),
(163, "Chives", "Allium schoenoprasum", "High", "Full sun", "Up to 30 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Chives.jpg/320px-Chives.jpg", "https://en.wikipedia.org/wiki/Chives"),
(164, "Cilantro", "Coriandrum sativum", "High", "Full sun", "Up to 50 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Coriander_plant.jpg/320px-Coriander_plant.jpg", "https://en.wikipedia.org/wiki/Cilantro"),
(165, "Dill", "Anethum graveolens", "Moderate", "Full sun", "Up to 60 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Dill_plant.jpg/320px-Dill_plant.jpg", "https://en.wikipedia.org/wiki/Dill"),
(166, "Lavender", "Lavandula angustifolia", "Low", "Full sun", "Up to 1 m", "Purple", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Lavender_flower.jpg/320px-Lavender_flower.jpg", "https://en.wikipedia.org/wiki/Lavender"),
(167, "Chamomile", "Matricaria chamomilla", "Low", "Full sun", "Up to 60 cm", "White/Yellow", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Chamomile_flowers.jpg/320px-Chamomile_flowers.jpg", "https://en.wikipedia.org/wiki/Chamomile"),
(168, "Echinacea", "Echinacea purpurea", "Moderate", "Full sun", "Up to 1.2 m", "Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Echinacea_purpurea_2.jpg/320px-Echinacea_purpurea_2.jpg", "https://en.wikipedia.org/wiki/Echinacea"),
(169, "Bee Balm", "Monarda didyma", "Moderate", "Full sun", "Up to 1 m", "Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Monarda_didyma.jpg/320px-Monarda_didyma.jpg", "https://en.wikipedia.org/wiki/Bee_balm"),
(170, "Lemon Balm", "Melissa officinalis", "Low", "Full sun", "Up to 60 cm", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Lemon_balm_plant.jpg/320px-Lemon_balm_plant.jpg", "https://en.wikipedia.org/wiki/Lemon_balm"),
(171, "Mint", "Mentha spicata", "Moderate", "Partial shade", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Spear_mint.jpg/320px-Spear_mint.jpg", "https://en.wikipedia.org/wiki/Mint"),
(172, "Pineapple", "Ananas comosus", "Moderate", "Full sun", "Up to 1.5 m", "Yellow", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Pineapple.jpg/320px-Pineapple.jpg", "https://en.wikipedia.org/wiki/Pineapple"),
(173, "Papaya", "Carica papaya", "Moderate", "Full sun", "Up to 3 m", "Orange", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Papaya_1.jpg/320px-Papaya_1.jpg", "https://en.wikipedia.org/wiki/Papaya"),
(174, "Mango", "Mangifera indica", "Moderate", "Full sun", "Up to 10 m", "Yellow/Red/Green", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Mangoes.jpg/320px-Mangoes.jpg", "https://en.wikipedia.org/wiki/Mango"),
(175, "Banana", "Musa spp.", "High", "Full sun", "Up to 3 m", "Yellow", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Musa_spp.jpg/320px-Musa_spp.jpg", "https://en.wikipedia.org/wiki/Banana"),
(176, "Coconut", "Cocos nucifera", "High", "Full sun", "Up to 30 m", "Brown", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Coconuts.jpg/320px-Coconuts.jpg", "https://en.wikipedia.org/wiki/Coconut"),
(177, "Dragon Fruit", "Hylocereus undatus", "Moderate", "Full sun", "Up to 3 m", "Pink", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Dragonfruit.jpg/320px-Dragonfruit.jpg", "https://en.wikipedia.org/wiki/Dragonfruit"),
(178, "Passion Fruit", "Passiflora edulis", "Moderate", "Full sun", "Up to 3 m", "Purple/Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Passion_fruit.jpg/320px-Passion_fruit.jpg", "https://en.wikipedia.org/wiki/Passionfruit"),
(179, "Avocado", "Persea americana", "Moderate", "Full sun", "Up to 20 m", "Green", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Avocado_tree.jpg/320px-Avocado_tree.jpg", "https://en.wikipedia.org/wiki/Avocado"),
(180, "Fig", "Ficus carica", "Moderate", "Full sun", "Up to 10 m", "Purple/Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Figs.jpg/320px-Figs.jpg", "https://en.wikipedia.org/wiki/Fig"),
(181, "Olive", "Olea europaea", "High", "Full sun", "Up to 10 m", "Green", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Olives.jpg/320px-Olives.jpg", "https://en.wikipedia.org/wiki/Olive"),
(182, "Pomegranate", "Punica granatum", "Moderate", "Full sun", "Up to 5 m", "Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Pomegranate_fruit.jpg/320px-Pomegranate_fruit.jpg", "https://en.wikipedia.org/wiki/Pomegranate"),
(183, "Blueberry", "Vaccinium corymbosum", "Moderate", "Full sun", "Up to 1 m", "Blue", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Blueberries.jpg/320px-Blueberries.jpg", "https://en.wikipedia.org/wiki/Blueberry"),
(184, "Strawberry", "Fragaria × ananassa", "High", "Full sun", "Up to 30 cm", "Red", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Strawberries.jpg/320px-Strawberries.jpg", "https://en.wikipedia.org/wiki/Strawberry"),
(185, "Raspberry", "Rubus idaeus", "Moderate", "Full sun", "Up to 1.5 m", "Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Raspberries.jpg/320px-Raspberries.jpg", "https://en.wikipedia.org/wiki/Raspberry"),
(186, "Blackberry", "Rubus fruticosus", "Moderate", "Full sun", "Up to 2 m", "Black", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Blackberries.jpg/320px-Blackberries.jpg", "https://en.wikipedia.org/wiki/Blackberry"),
(187, "Cantaloupe", "Cucumis melo", "High", "Full sun", "Up to 1.5 m", "Orange", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Cantaloupe.jpg/320px-Cantaloupe.jpg", "https://en.wikipedia.org/wiki/Cantaloupe"),
(188, "Watermelon", "Citrullus lanatus", "High", "Full sun", "Up to 2 m", "Green/Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Watermelon_1.jpg/320px-Watermelon_1.jpg", "https://en.wikipedia.org/wiki/Watermelon"),
(189, "Honeydew", "Cucumis melo", "High", "Full sun", "Up to 1 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Honeydew_melon.jpg/320px-Honeydew_melon.jpg", "https://en.wikipedia.org/wiki/Honeydew_melon"),
(190, "Fig", "Ficus carica", "Moderate", "Full sun", "Up to 10 m", "Purple/Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Figs.jpg/320px-Figs.jpg", "https://en.wikipedia.org/wiki/Fig"),
(191, "Grapefruit", "Citrus × paradisi", "Moderate", "Full sun", "Up to 4 m", "Yellow/Red", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Redgrapefruit.jpg/320px-Redgrapefruit.jpg", "https://en.wikipedia.org/wiki/Grapefruit"),
(192, "Lemon", "Citrus limon", "High", "Full sun", "Up to 3 m", "Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Lemon_1.jpg/320px-Lemon_1.jpg", "https://en.wikipedia.org/wiki/Lemon"),
(193, "Lime", "Citrus aurantiifolia", "High", "Full sun", "Up to 3 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Limes.jpg/320px-Limes.jpg", "https://en.wikipedia.org/wiki/Lime"),
(194, "Orange", "Citrus sinensis", "High", "Full sun", "Up to 5 m", "Orange", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Orange_blossoms.jpg/320px-Orange_blossoms.jpg", "https://en.wikipedia.org/wiki/Orange"),
(195, "Tangerine", "Citrus reticulata", "High", "Full sun", "Up to 4 m", "Orange", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Tangerines.jpg/320px-Tangerines.jpg", "https://en.wikipedia.org/wiki/Tangerine"),
(196, "Clementine", "Citrus × clementina", "High", "Full sun", "Up to 3 m", "Orange", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Clementine_Oranges.jpg/320px-Clementine_Oranges.jpg", "https://en.wikipedia.org/wiki/Clementine"),
(197, "Grapes", "Vitis vinifera", "High", "Full sun", "Up to 3 m", "Green/Red/Black", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Grapes.jpg/320px-Grapes.jpg", "https://en.wikipedia.org/wiki/Grape"),
(198, "Cherries", "Prunus avium", "High", "Full sun", "Up to 3 m", "Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Cherries.jpg/320px-Cherries.jpg", "https://en.wikipedia.org/wiki/Cherry"),
(199, "Peach", "Prunus persica", "High", "Full sun", "Up to 5 m", "Pink", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Peach.jpg/320px-Peach.jpg", "https://en.wikipedia.org/wiki/Peach"),
(200, "Plum", "Prunus domestica", "High", "Full sun", "Up to 5 m", "Purple/Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Plums.jpg/320px-Plums.jpg", "https://en.wikipedia.org/wiki/Plum"),
(201, "Apricot", "Prunus armeniaca", "High", "Full sun", "Up to 4 m", "Orange", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Apricots.jpg/320px-Apricots.jpg", "https://en.wikipedia.org/wiki/Apricot"),
(202, "Nectarine", "Prunus persica var. nucipersica", "High", "Full sun", "Up to 5 m", "Red/Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Nectarines.jpg/320px-Nectarines.jpg", "https://en.wikipedia.org/wiki/Nectarine"),
(203, "Mulberry", "Morus spp.", "Moderate", "Full sun", "Up to 10 m", "Red/Black/White", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Mulberry_fruits.jpg/320px-Mulberry_fruits.jpg", "https://en.wikipedia.org/wiki/Mulberry"),
(204, "Kiwi", "Actinidia deliciosa", "Moderate", "Full sun", "Up to 3 m", "Brown/Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Kiwifruit.jpg/320px-Kiwifruit.jpg", "https://en.wikipedia.org/wiki/Kiwifruit"),
(205, "Cranberry", "Vaccinium macrocarpon", "Moderate", "Full sun", "Up to 30 cm", "Red", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Cranberries.jpg/320px-Cranberries.jpg", "https://en.wikipedia.org/wiki/Cranberry"),
(206, "Goji Berry", "Lycium barbarum", "High", "Full sun", "Up to 1.5 m", "Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Goji_berries.jpg/320px-Goji_berries.jpg", "https://en.wikipedia.org/wiki/Goji_berry"),
(207, "Hops", "Humulus lupulus", "High", "Full sun", "Up to 6 m", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Hops.jpg/320px-Hops.jpg", "https://en.wikipedia.org/wiki/Hops"),
(208, "Elderberry", "Sambucus nigra", "Moderate", "Full sun", "Up to 5 m", "Black/Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Sambucus_nigra_%28berries%29.jpg/320px-Sambucus_nigra_%28berries%29.jpg", "https://en.wikipedia.org/wiki/Elderberry"),
(209, "Jackfruit", "Artocarpus heterophyllus", "Moderate", "Full sun", "Up to 20 m", "Green/Yellow", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Jackfruit.jpg/320px-Jackfruit.jpg", "https://en.wikipedia.org/wiki/Jackfruit"),
(210, "Durian", "Durio spp.", "Moderate", "Full sun", "Up to 25 m", "Green", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Durian_%28fruit%29.jpg/320px-Durian_%28fruit%29.jpg", "https://en.wikipedia.org/wiki/Durian"),
(211, "Tamarind", "Tamarindus indica", "Moderate", "Full sun", "Up to 15 m", "Brown", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Tamarindus_indica_fruit.jpg/320px-Tamarindus_indica_fruit.jpg", "https://en.wikipedia.org/wiki/Tamarind"),
(212, "Lychee", "Litchi chinensis", "Moderate", "Full sun", "Up to 12 m", "Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Litchi.jpg/320px-Litchi.jpg", "https://en.wikipedia.org/wiki/Lychee"),
(213, "Longan", "Dimocarpus longan", "Moderate", "Full sun", "Up to 15 m", "Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Longan_fruit.jpg/320px-Longan_fruit.jpg", "https://en.wikipedia.org/wiki/Longan"),
(214, "Starfruit", "Averrhoa carambola", "Moderate", "Full sun", "Up to 5 m", "Yellow/Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Starfruit.jpg/320px-Starfruit.jpg", "https://en.wikipedia.org/wiki/Starfruit"),
(215, "Sapodilla", "Manilkara zapota", "Moderate", "Full sun", "Up to 15 m", "Brown", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Sapodilla.jpg/320px-Sapodilla.jpg", "https://en.wikipedia.org/wiki/Sapodilla"),
(216, "Guava", "Psidium guajava", "Moderate", "Full sun", "Up to 5 m", "Green/Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Guava_fruit.jpg/320px-Guava_fruit.jpg", "https://en.wikipedia.org/wiki/Guava"),
(217, "Date", "Phoenix dactylifera", "High", "Full sun", "Up to 20 m", "Brown", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Dates.jpg/320px-Dates.jpg", "https://en.wikipedia.org/wiki/Date_palm"),
(218, "Date Palm", "Phoenix dactylifera", "High", "Full sun", "Up to 20 m", "Green", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Date_palms.jpg/320px-Date_palms.jpg", "https://en.wikipedia.org/wiki/Date_palm"),
(219, "Coconut Palm", "Cocos nucifera", "High", "Full sun", "Up to 30 m", "Green", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Cocos_nucifera.jpg/320px-Cocos_nucifera.jpg", "https://en.wikipedia.org/wiki/Coconut"),
(220, "Aloe Vera", "Aloe barbadensis miller", "Low", "Full sun", "Up to 1 m", "Green", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Aloe_vera.jpg/320px-Aloe_vera.jpg", "https://en.wikipedia.org/wiki/Aloe_vera"),
(221, "Cactus", "Cactaceae", "Low", "Full sun", "Up to 1.5 m", "Green", "Slow", "Water infrequently", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Cactus.jpg/320px-Cactus.jpg", "https://en.wikipedia.org/wiki/Cactus"),
(222, "Pine Tree", "Pinus spp.", "High", "Full sun", "Up to 30 m", "Green", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Pinus.jpg/320px-Pinus.jpg", "https://en.wikipedia.org/wiki/Pine"),
(223, "Fir Tree", "Abies spp.", "High", "Full sun", "Up to 30 m", "Green", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Fir_tree.jpg/320px-Fir_tree.jpg", "https://en.wikipedia.org/wiki/Fir"),
(224, "Spruce Tree", "Picea spp.", "High", "Full sun", "Up to 30 m", "Green", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Spruce_tree.jpg/320px-Spruce_tree.jpg", "https://en.wikipedia.org/wiki/Spruce"),
(225, "Cedar Tree", "Cedrus spp.", "High", "Full sun", "Up to 30 m", "Green", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Cedar.jpg/320px-Cedar.jpg", "https://en.wikipedia.org/wiki/Cedar"),
(226, "Redwood", "Sequoia sempervirens", "High", "Full sun", "Up to 115 m", "Red", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Redwood.jpg/320px-Redwood.jpg", "https://en.wikipedia.org/wiki/Redwood"),
(227, "Sequoia", "Sequoiadendron giganteum", "High", "Full sun", "Up to 90 m", "Green", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Sequoia.jpg/320px-Sequoia.jpg", "https://en.wikipedia.org/wiki/Sequoia"),
(228, "Bamboo", "Bambusoideae", "High", "Full sun", "Up to 40 m", "Green", "Fast", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Bamboo_forest.jpg/320px-Bamboo_forest.jpg", "https://en.wikipedia.org/wiki/Bamboo"),
(229, "Banana Palm", "Musa spp.", "High", "Full sun", "Up to 10 m", "Green", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Banana_palm.jpg/320px-Banana_palm.jpg", "https://en.wikipedia.org/wiki/Banana"),
(230, "Palm Tree", "Arecaceae", "High", "Full sun", "Up to 30 m", "Green", "Slow", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Palm_tree.jpg/320px-Palm_tree.jpg", "https://en.wikipedia.org/wiki/Palm_tree"),
(231, "Hibiscus", "Hibiscus spp.", "High", "Full sun", "Up to 3 m", "Red", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Hibiscus_syriacus_%28Rose_of_Sharon%29.jpg/320px-Hibiscus_syriacus_%28Rose_of_Sharon%29.jpg", "https://en.wikipedia.org/wiki/Hibiscus"),
(232, "Bougainvillea", "Bougainvillea spp.", "High", "Full sun", "Up to 12 m", "Purple/Red/Orange", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Bougainvillea_2.jpg/320px-Bougainvillea_2.jpg", "https://en.wikipedia.org/wiki/Bougainvillea"),
(233, "Jasmine", "Jasminum spp.", "Moderate", "Full sun", "Up to 2 m", "White/Yellow/Pink", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Jasmine.jpg/320px-Jasmine.jpg", "https://en.wikipedia.org/wiki/Jasmine"),
(234, "Lavender", "Lavandula spp.", "High", "Full sun", "Up to 1 m", "Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Lavender_bush.jpg/320px-Lavender_bush.jpg", "https://en.wikipedia.org/wiki/Lavender"),
(235, "Rose", "Rosa spp.", "High", "Full sun", "Up to 2 m", "Red/Pink/Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Rose_in_full_bloom.jpg/320px-Rose_in_full_bloom.jpg", "https://en.wikipedia.org/wiki/Rose"),
(236, "Daisy", "Bellis perennis", "Moderate", "Full sun", "Up to 30 cm", "White/Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Daisy_flowers.jpg/320px-Daisy_flowers.jpg", "https://en.wikipedia.org/wiki/Daisy"),
(237, "Tulip", "Tulipa spp.", "High", "Full sun", "Up to 70 cm", "Red/Yellow/Pink", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Tulip_fields_in_Lisse_3.jpg/320px-Tulip_fields_in_Lisse_3.jpg", "https://en.wikipedia.org/wiki/Tulip"),
(238, "Sunflower", "Helianthus annuus", "High", "Full sun", "Up to 3 m", "Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Sunflower_%28Helianthus_annuus%29.jpg/320px-Sunflower_%28Helianthus_annuus%29.jpg", "https://en.wikipedia.org/wiki/Sunflower"),
(239, "Orchid", "Orchidaceae", "High", "Partial sun", "Up to 1.5 m", "White/Pink/Purple", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Orchid_flower.jpg/320px-Orchid_flower.jpg", "https://en.wikipedia.org/wiki/Orchid"),
(240, "Iris", "Iris spp.", "Moderate", "Full sun", "Up to 1 m", "Purple/Blue/Yellow", "Moderate", "Water regularly", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Iris_germanica.jpg/320px-Iris_germanica.jpg", "https://en.wikipedia.org/wiki/Iris")
]

c.executemany("INSERT OR IGNORE INTO plants VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", plants)
conn.commit()

weather_codes = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
    55: "Dense drizzle", 61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    80: "Rain showers", 95: "Thunderstorm"
}

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weathercode"
    try:
        res = requests.get(url)
        data = res.json()
        temp = data['current']['temperature_2m']
        code = data['current']['weathercode']
        description = weather_codes.get(code, "Unknown")
        return f"{description}, {temp}°C"
    except:
        return "Weather not available"

class PlantApp:
    def __init__(self, master):
        self.master = master
        master.title("HerbifyDH")
        master.configure(bg='#0d1117')
        self.set_style()

        self.sidebar = tk.Frame(master, bg='#161b22', width=250, bd=0, highlightthickness=0)
        self.sidebar.pack(side='left', fill='y')

        self.rightbar = tk.Frame(master, bg='#161b22', width=200, bd=0, highlightthickness=0)
        self.rightbar.pack(side='right', fill='y')

        self.top_center = tk.Frame(master, bg='#161b22', bd=0, highlightthickness=0)
        self.top_center.pack(fill='x')

        self.main_center = tk.Frame(master, bg='#0d1117', bd=0, highlightthickness=0)
        self.main_center.pack(fill='both', expand=True)

        # Sidebar: My Plants
        tk.Label(self.sidebar, text="My Plants", font=self.font_bold, fg='white', bg='#161b22').pack(pady=10)
        self.my_plants_listbox = tk.Listbox(self.sidebar, bg='#0d1117', fg='white', font=self.font, bd=0, highlightthickness=0)
        self.my_plants_listbox.pack(fill='both', expand=True, padx=5)
        self.my_plants_listbox.bind("<Double-1>", self.open_plant_profile)

        # Search
        tk.Label(self.top_center, text="Find a plant", bg='#161b22', fg='white', font=self.font_bold).pack(pady=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_plant_list)
        self.search_entry = tk.Entry(self.top_center, textvariable=self.search_var, bg='#30363d', fg='white', font=self.font)
        self.search_entry.pack(fill='x', padx=8, pady=4)

        self.plant_listbox = tk.Listbox(self.main_center, bg='#0d1117', fg='white', font=self.font, bd=0, highlightthickness=0)
        self.plant_listbox.pack(fill='both', expand=True, padx=8, pady=(5, 2))
        self.plant_listbox.bind('<<ListboxSelect>>', self.select_plant)

        self.description_label = tk.Label(self.main_center, text="", bg='#0d1117', fg='#999', wraplength=350, justify='left', font=self.font)
        self.description_label.pack(padx=10, pady=(0, 5), anchor="w")

        tk.Button(self.main_center, text="Add Plant", command=self.add_plant_to_profile, bg='#238636', fg='white', font=self.font_bold).pack(fill='x', padx=8)

        # Rightbar
        self.plant_of_day_label = tk.Label(self.rightbar, text="", bg='#161b22', fg='#2ea043', wraplength=180, justify='left', font=self.font)
        self.plant_of_day_label.pack(pady=10, padx=5)

        self.weather_label = tk.Label(self.rightbar, text="Weather: ", bg='#161b22', fg='#2ea043', font=self.font)
        self.weather_label.pack(pady=5)

        self.water_label = tk.Label(self.rightbar, text="Watering Schedule", bg='#161b22', fg='white', font=self.font_bold)
        self.water_label.pack(pady=5)

        self.watering_list = tk.Listbox(self.rightbar, bg='#0d1117', fg='white', font=self.font, bd=0, highlightthickness=0)
        self.watering_list.pack(fill='both', expand=True, padx=5, pady=(0, 10))

        self.load_plants()
        self.show_plant_of_the_day()
        self.show_my_plants()
        self.update_weather()

    def set_style(self):
        self.font = ("Segoe UI", 10)
        self.font_bold = ("Segoe UI", 10, "bold")

    def load_plants(self):
        c.execute("SELECT name FROM plants")
        self.all_plants = [row[0] for row in c.fetchall()]
        self.update_plant_list()

    def update_plant_list(self, *args):
        search = self.search_var.get().lower()
        self.plant_listbox.delete(0, tk.END)
        for plant in self.all_plants:
            if search in plant.lower():
                self.plant_listbox.insert(tk.END, plant)
        self.description_label.config(text="")

    def select_plant(self, event):
        selection = self.plant_listbox.curselection()
        if selection:
            self.selected_plant_name = self.plant_listbox.get(selection[0])
            c.execute("SELECT * FROM plants WHERE name=?", (self.selected_plant_name,))
            plant = c.fetchone()
            if plant:
                self.description_label.config(
                    text=f"{plant[2]}\nWatering: {plant[3]} | Light: {plant[4]}\n{plant[8]}"
                )

    def add_plant_to_profile(self):
        if not hasattr(self, 'selected_plant_name'):
            return
        lat, lon = 51.5074, -0.1278
        c.execute("SELECT id FROM plants WHERE name=?", (self.selected_plant_name,))
        plant_id = c.fetchone()[0]
        next_water = (datetime.now() + timedelta(days=3)).isoformat()
        c.execute("INSERT INTO user_plants (plant_id, latitude, longitude, next_water_time) VALUES (?, ?, ?, ?)",
                  (plant_id, lat, lon, next_water))
        conn.commit()
        self.show_my_plants()

    def show_my_plants(self):
        self.my_plants_listbox.delete(0, tk.END)
        self.watering_list.delete(0, tk.END)
        c.execute("SELECT user_plants.id, plants.name, user_plants.next_water_time, user_plants.custom_name FROM user_plants JOIN plants ON user_plants.plant_id = plants.id")
        self.my_plants = c.fetchall()
        for i, (pid, name, water_time, custom_name) in enumerate(self.my_plants, 1):
            label = custom_name if custom_name else name
            due = datetime.fromisoformat(water_time)
            note = " (Water Today)" if datetime.now() >= due else ""
            self.my_plants_listbox.insert(tk.END, f"#{i}: {label}{note}")
            self.watering_list.insert(tk.END, f"{label} - Next: {due.strftime('%b %d')}")

    def open_plant_profile(self, event):
        index = self.my_plants_listbox.curselection()
        if not index:
            return
        i = index[0]
        pid, name, water_time, custom_name = self.my_plants[i]
        c.execute("SELECT * FROM plants WHERE name=?", (name,))
        plant = c.fetchone()

        popup = tk.Toplevel(self.master)
        popup.title(f"{name} Profile")
        popup.configure(bg='#0d1117')

        box = tk.Frame(popup, bg='#161b22', bd=0)
        box.pack(padx=10, pady=10, fill='both', expand=True)

        wiki = tk.Label(box, text="Wikipedia Page", fg='cyan', bg='#161b22', cursor="hand2", font=self.font)
        wiki.pack()
        wiki.bind("<Button-1>", lambda e: webbrowser.open(plant[10]))

        details = f"""
Name: {plant[1]}
Scientific: {plant[2]}
Watering: {plant[3]}
Sunlight: {plant[4]}
Height: {plant[5]}
Color: {plant[6]}
Growth: {plant[7]}
Care: {plant[8]}
"""
        tk.Label(box, text=details.strip(), justify="left", fg='white', bg='#161b22', font=self.font).pack()

        rename_entry = tk.Entry(box, fg='white', bg='#0d1117', font=self.font)
        rename_entry.insert(0, custom_name if custom_name else plant[1])
        rename_entry.pack(pady=2)

        tk.Button(box, text="Rename", command=lambda: self.rename_plant(pid, rename_entry.get(), popup),
                  bg='#238636', fg='white', font=self.font).pack(pady=2)
        tk.Button(box, text="Remove Plant", command=lambda: self.remove_plant(pid, popup),
                  bg='#da3633', fg='white', font=self.font).pack(pady=2)

    def rename_plant(self, pid, new_name, win):
        c.execute("UPDATE user_plants SET custom_name=? WHERE id=?", (new_name, pid))
        conn.commit()
        win.destroy()
        self.show_my_plants()

    def remove_plant(self, pid, win):
        c.execute("DELETE FROM user_plants WHERE id=?", (pid,))
        conn.commit()
        win.destroy()
        self.show_my_plants()

    def show_plant_of_the_day(self):
        c.execute("SELECT * FROM plants WHERE name=?", ("Cooksonia",))
        plant = c.fetchone()
        if plant:
            self.plant_of_day_label.config(text=f'''🌿 Plant of the Day:🌿

Cooksonia:
The Cooksonia is an extinct genus of primitive
vascular plants from the Silurian period.
It is considered one of the earliest known
land plants with a simple branching structure
and no true leaves or roots.''')

    def update_weather(self):
        weather = get_weather(51.5074, -0.1278)
        self.weather_label.config(text=f"Weather: {weather}")

# --- Run Application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PlantApp(root)
    root.mainloop()
