import React from "react";

const Card = ({ title, words }) => {
    return (
        <div className="max-w-sm rounded overflow-hidden shadow-xl m-4">
            <div className="max-w-sm rounded p-4 shadow-md shadow-cyan-300">
                <div className="font-bold text-xl mb-2 text-center">{title}</div>
            </div>
            <div className="px-6 py-4">
                {words && (
                    <ul>
                        {words.map((word, index) => (
                            <li key={index} className="mb-2">{word}</li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
};

export default Card;