import React, { useEffect, useState } from 'react';

type Dog = {
    breed: string;
    image?: string;
};

type DogResponse = {
    data: Dog[];
    page: number;
    next_page?: number;
    total: number;
}

type DogListPageProps = {
    limit?: number;
}

export const DogListPage: React.FC<DogListPageProps> = ({ limit = 15 }) => {
    const [dogs, setDogs] = useState<Dog[]>([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [nextPage, setNextPage] = useState<number | null>(null)


    useEffect(() => {
        const fetchDogs = async () => {
            try {
                const response = await fetch(`http://localhost:8000/dogs?page=${currentPage}&limit=${limit}`);
                const data: DogResponse = await response.json();
                setDogs(data.data);
                setNextPage(data.next_page || null);
            } catch (error) {

            }
        };

        fetchDogs();
    }, [currentPage, limit]);

    return (
        <div>
            <h1>Dog List</h1>
            <ul>
                {dogs.map(dog => (
                    <li key={dog.breed}>
                        <img src={dog.image} alt={dog.breed} />
                        <p>{dog.breed}</p>
                    </li>
                ))}
            </ul>
            <button onClick={() => setCurrentPage(currentPage - 1)} disabled={currentPage === 1}>Previous</button>
            <button onClick={() => {
                if (nextPage!== null) {
                    setCurrentPage(nextPage)
                }
                }} disabled={nextPage === null}>Next</button>
        </div>
    );
}