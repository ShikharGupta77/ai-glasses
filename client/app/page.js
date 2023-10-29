"use client";
import { useState, useEffect } from "react";
import axios from "axios";

export default function Home() {
  const [transcript, setTranscript] = useState(""); // Initialize with an empty string or the appropriate default value
  const [facts, setFacts] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/transcript");
        setTranscript(response.data); // Update the responseData state with the response data
        //console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    const interval = setInterval(fetchData, 2000); // Fetch data every 2 seconds

    return () => clearInterval(interval); // Cleanup to clear the interval when the component unmounts
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/facts");
        console.log(response);
        setFacts(response.data); // Update the responseData state with the response data
        //console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    const interval = setInterval(fetchData, 2000); // Fetch data every 2 seconds

    return () => clearInterval(interval); // Cleanup to clear the interval when the component unmounts
  }, []);

  return (
    <main className="flex h-screen flex-row items-center bg-primary">
      <div className="flex h-full w-[65%] justify-center items-center">
        <div className="flex flex-col bg-secondary w-[90%] h-[90%] rounded-2xl pt-3 text-accent">
          <p className=" flex-col text-6xl font-bold self-center mt-6">Transcript</p>
          <div className="pl-12 pt-14 text-xl">
            <ul>{transcript}</ul>
          </div>
        </div>
      </div>
      <div className="flex h-full w-[35%] justify-center items-center">
        <div className="flex flex-col bg-secondary w-[90%] h-[90%] rounded-2xl pt-3 text-accent">
          <p className=" flex-col text-6xl font-bold self-center mt-6">Facts</p>
          <div className="pl-12 pt-14 text-xl">{facts}</div>
        </div>
      </div>
    </main>
  );
}
