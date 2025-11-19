"use client";
import axios from "axios";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { toast } from "sonner";
import { jwtDecoder } from "@/utils/jwtDecoder";
import { jwtFormat } from "@/utils/jwtFormat";

type BookData = {
  title: string;
  authors?: string[];
  isbn?: string;
  thumbnail: string;
};

export default function Page() {
  const params = useParams();
  const router = useRouter();

  const [isbnInput, setIsbnInput] = useState("");
  const [book, setBook] = useState<BookData | null>(null);
  const [loading, setLoading] = useState(false);
  const [returnDays, setReturnDays] = useState(1);
  const [fullName, setFullName] = useState("");
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const token = params.student as string;
    if (!token || !jwtFormat(token)) {
      toast.error("You are not a student", { duration: 1200 });
      setTimeout(() => router.push("/"), 1200);
      return;
    }
    const decoded = jwtDecoder(token);
    setFullName(decoded?.fullname || "");
  }, [params.book, router]);

  const toISBN13 = (isbn: string) => {
    isbn = isbn.replace(/[-\s]/g, "");
    if (isbn.length === 10) {
      isbn = "978" + isbn.slice(0, 9);
      let sum = 0;
      for (let i = 0; i < 12; i++) {
        sum += parseInt(isbn[i]) * (i % 2 === 0 ? 1 : 3);
      }
      const check = (10 - (sum % 10)) % 10;
      isbn += check.toString();
    }
    return isbn;
  };

  const validateISBN = (isbn: string) => {
    return /^(97[89]\d{10}|\d{9}[\dX])$/.test(isbn);
  };

  const handleFetchBook = async () => {
    // remove spaces and dashes
    const isbn = isbnInput.trim().replace(/[-\s]/g, "");

    // check if isbn is valid
    if (!validateISBN(isbn)) {
      toast.error("Invalid ISBN (10 or 13 digits).");
      return;
    }

    const isbn13 = toISBN13(isbn);
    setLoading(true);

    try {
      const res = await axios.get(
        `https://www.googleapis.com/books/v1/volumes?q=isbn:${isbn13}`,
      );

      if (!res.data.items?.length) {
        toast.error("Book not found.");
        setBook(null);
        return;
      }

      const info = res.data.items[0].volumeInfo;
      const isbnObj = info.industryIdentifiers?.find(
        (id: any) => id.type === "ISBN_13" || id.type === "ISBN_10",
      );

      setBook({
        title: info.title,
        authors: info.authors,
        isbn: isbnObj?.identifier || isbnInput,
        thumbnail: info.imageLinks?.thumbnail,
      });

      setShowModal(true); // open modal
    } catch (err) {
      toast.error("Failed to fetch book info.", { duration: 1200 });
      setBook(null);
    } finally {
      setLoading(false);
    }
  };
  const handleSubmit = async () => {
    if (!book) {
      toast.error("No book selected.");
      return;
    }

    if (!params.student) {
      toast.error("Student token missing.");
      return;
    }
    console.log(book);
    if (!book.isbn) {
      toast.error("Book ISBN missing.");
      return;
    }

    const nonWorkingDays = [0, 6];
    let remaining = returnDays;
    const returnDate = new Date();

    while (remaining > 0) {
      returnDate.setDate(returnDate.getDate() + 1);
      if (!nonWorkingDays.includes(returnDate.getDay())) remaining--;
    }

    const payload = {
      token: params.student,
      isbn: book.isbn,
      bookname: book.title,
      bookauthor: book.authors?.join(", ") || "Unknown",
      returndays: returnDays,
    };

    console.log("Borrow payload:", payload); // sanity check

    try {
      const res = await axios.post("http://localhost:8000/borrow", payload);
      toast.success(res.data.message);
      resetStateAfterSubmit();
      router.push("/qr");
    } catch (err) {
      handleBorrowError(err);
    }
  };

  // --- helpers ---

  function resetStateAfterSubmit() {
    setBook(null);
    setIsbnInput("");
    setReturnDays(1);
    setShowModal(false);
  }

  function handleBorrowError(err: unknown) {
    if (axios.isAxiosError(err)) {
      const detail = err.response?.data?.detail;

      if (err.response?.status === 400) {
        const message =
          typeof detail === "string"
            ? detail
            : detail?.msg || detail?.[0]?.msg || "Invalid request.";

        toast.error(message, { duration: 1200 });
        resetStateAfterSubmit();
        return;
      }

      const message =
        typeof detail === "string"
          ? detail
          : detail?.msg || detail?.[0]?.msg || "Request failed.";

      toast.error(message, { duration: 1200 });
      return;
    }

    toast.error("Failed to borrow the book. Try again.", { duration: 1200 });
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 py-8 gap-6 bg-[var(--color-dark)] text-[var(--color-light)]">
      <h1 className="text-2xl font-semibold">
        What book do you want to borrow? <br /> {fullName}
      </h1>

      <div className="flex flex-col gap-2 w-full max-w-md">
        <input
          type="text"
          placeholder="Enter ISBN"
          className="px-4 py-2 rounded-md bg-[var(--color-dark)] border border-white/20 placeholder:text-white/50 focus:outline-none focus:border-white/50"
          value={isbnInput}
          onChange={(e) => setIsbnInput(e.target.value)}
        />
        <button
          onClick={handleFetchBook}
          disabled={loading}
          className="px-4 py-2 rounded-md bg-white/10 hover:bg-white/20 transition-colors font-medium"
        >
          {loading ? "Finding book..." : "Find Book"}
        </button>
      </div>

      {/* Modal */}
      {showModal && book && (
        <div className="fixed inset-0 flex items-center justify-center bg-black/50 z-50">
          <div className="bg-[var(--color-dark)] text-[var(--color-light)] rounded-lg p-6 w-full max-w-md relative">
            <button
              onClick={() => setShowModal(false)}
              className="absolute top-3 right-3 text-white/50 hover:text-white transition-colors"
            >
              ✕
            </button>
            <img
              src={book.thumbnail}
              alt="book"
              className="w-32 h-auto rounded mx-auto mb-4"
            />
            <p>
              <span className="font-semibold">Title:</span> {book.title}
            </p>
            {book.authors && (
              <p>
                <span className="font-semibold">Authors:</span>{" "}
                {book.authors.join(", ")}
              </p>
            )}
            {book.isbn && (
              <p>
                <span className="font-semibold">ISBN:</span> {book.isbn}
              </p>
            )}

            <div className="flex items-center gap-2 mt-2">
              <label className="font-semibold">Return in days:</label>
              <select
                value={returnDays}
                onChange={(e) => setReturnDays(Number(e.target.value))}
                className="px-2 py-1 rounded-md bg-[var(--color-dark)] border border-white/20 focus:outline-none"
              >
                <option value={1}>1</option>
                <option value={2}>2</option>
                <option value={3}>3</option>
              </select>
            </div>

            <button
              onClick={handleSubmit}
              className="mt-4 w-full px-4 py-2 rounded-md bg-white/10 hover:bg-white/20 font-medium transition-colors"
            >
              Confirm Borrow
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
