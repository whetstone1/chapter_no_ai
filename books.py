import os

BOOKS = [
    {"title": "The Count of Monte Cristo", "author": "Alexandre Dumas", "id": "1184"},
    {"title": "Vanity Fair", "author": "William Makepeace Thackeray", "id": "599"},
    {"title": "Uncle Tom’s Cabin", "author": "Harriet Beecher Stowe", "id": "203"},
    {"title": "North and South", "author": "Elizabeth Gaskell", "id": "4276"},
    {"title": "Madame Bovary", "author": "Gustave Flaubert", "id": "2413"},
    {"title": "The Woman in White", "author": "Wilkie Collins", "id": "583"},
    {"title": "A Tale of Two Cities", "author": "Charles Dickens", "id": "98"},
    {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "id": "2554"},
    {"title": "20,000 Leagues Under the Sea", "author": "Jules Verne", "id": "164"},
    {"title": "Middlemarch", "author": "George Eliot", "id": "145"},
    {"title": "Anna Karenina", "author": "Leo Tolstoy", "id": "1399"},
    {"title": "War and Peace", "author": "Leo Tolstoy", "id": "2600"},
    {"title": "The Portrait of a Lady", "author": "Henry James", "id": "2833"},
    {"title": "Treasure Island", "author": "Robert Louis Stevenson", "id": "120"},
    {"title": "Tess of D’Ubervilles", "author": "Thomas Hardy", "id": "110"},
    {"title": "The War of the Worlds", "author": "HG Wells", "id": "36"},
    {"title": "Heart of Darkness", "author": "Joseph Conrad", "id": "219"},
    {"title": "The Hound of the Baskervilles", "author": "Sir Arthur Conan Doyle", "id": "2852"},
    {"title": "The Jungle", "author": "Upton Sinclair", "id": "140"},
    {"title": "The Nine-tailed Turtle", "author": "Zhang Chunfan", "id": "2868"},
    {"title": "The Phantom of the Opera", "author": "Gaston Leroux", "id": "175"},
    {"title": "The Secret Garden", "author": "Frances Hodgson Burnett", "id": "17396"},
    {"title": "Ulysses", "author": "James Joyce", "id": "4300"},
    {"title": "The Pickwick Papers", "author": "Charles Dickens", "id": "580"},
    {"title": "A Tale of Two Cities", "author": "Charles Dickens", "id": "98"},
    {"title": "Oliver Twist", "author": "Charles Dickens", "id": "730"},
    {"title": "A Christmas Carol", "author": "Charles Dickens", "id": "46"},
    {"title": "David Copperfield", "author": "Charles Dickens", "id": "766"},
    {"title": "Great Expectations", "author": "Charles Dickens", "id": "1400"},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "id": "1342"},
    {"title": "Sense and Sensibility", "author": "Jane Austen", "id": "161"},
    {"title": "Mansfield Park", "author": "Jane Austen", "id": "141"},
    {"title": "Emma", "author": "Jane Austen", "id": "158"},
    {"title": "Jane Eyre", "author": "Charlotte Bronte", "id": "1260"},
    {"title": "Wuthering Heights", "author": "Emily Bronte", "id": "768"},
    {"title": "The Hunchback of Notre Dame", "author": "Victor Hugo", "id": "125"},
    {"title": "Les Miserables", "author": "Victor Hugo", "id": "135"},
    {"title": "Frankenstein", "author": "Mary Shelley", "id": "84"},
    {"title": "Dracula", "author": "Bram Stoker", "id": "345"},
    {"title": "The Adventures of Sherlock Holmes", "author": "Sir Arthur Conan Doyle", "id": "1661"},
    {"title": "The Hound of the Baskervilles", "author": "Sir Arthur Conan Doyle", "id": "2852"},
    {"title": "Don Quixote", "author": "Miguel de Cervantes", "id": "996"},
    {"title": "In Search of Lost Time", "author": "Marcel Proust", "id": "1050"},
    {"title": "The Idiot", "author": "Fyodor Dostoevsky", "id": "2638"},
    {"title": "The Brothers Karamazov", "author": "Fyodor Dostoevsky", "id": "28054"},
    {"title": "Demons", "author": "Fyodor Dostoevsky", "id": "8117"},
]