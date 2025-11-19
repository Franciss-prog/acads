"use client";
import axios from "axios";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { toast } from "sonner";
import { jwtDecoder } from "@/utils/jwtDecoder";
import { jwtFormat } from "@/utils/jwtFormat";

type BorrowedBook = {
  title: string;
  authors?: string[];
  isbn: string;
  thumbnail?: string;
  borrowed_date?: string;
};

export default function ReturnBook() {
  const params = useParams();
  const router = useRouter();

  const [fullName, setFullName] = useState("");
  const [book, setBook] = useState<BorrowedBook | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = params.student as string;
    if (!token || !jwtFormat(token)) {
      toast.error("You are not a student", { duration: 1200 });
      setTimeout(() => router.push("/"), 1200);
      return;
    }
    const decoded = jwtDecoder(token);
    setFullName(decoded?.fullname || "");
    fetchBorrowedBook(token);
  }, [params.student, router]);

  const fetchBorrowedBook = async (token: string) => {
    try {
      const res = await axios.post(`http://localhost:8000/borrowed`, { token });

      if (!res.data.borrowed) {
        toast.info("No borrowed books found.", { duration: 1200 });
        setTimeout(() => router.push("/qr"), 1200);
        return;
      }

      const data = res.data.books;
      setBook({
        title: data.bookname,
        authors: data.bookauthor?.split(", "),
        isbn: data.isbn,
        thumbnail: data.thumbnail,
        borrowed_date: data.borrowed_date,
      });
    } catch (err) {
      toast.error("Failed to fetch borrowed book.", { duration: 1200 });
      setTimeout(() => router.push("/"), 1200);
    } finally {
      setLoading(false);
    }
  };

  const handleReturn = async () => {
    if (!book) return toast.error("No borrowed book to return.");

    try {
      const res = await axios.post(`http://localhost:8000/returnbook `, {
        token: params.student,
        isbn: book.isbn,
      });
      toast.success(res.data.message || "Book returned successfully!");
      setTimeout(() => router.push("/qr"), 1200);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        toast.error(err.response?.data?.detail || "Return failed.", {
          duration: 1200,
        });
        return;
      }
      toast.error("Failed to return book. Try again.", { duration: 1200 });
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[var(--color-dark)] text-[var(--color-light)]">
        <p>Checking borrowed books...</p>
      </div>
    );
  }

  if (!book) return null;

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 py-8 gap-6 bg-[var(--color-dark)] text-[var(--color-light)]">
      <h1 className="text-2xl font-semibold text-center">
        Return borrowed book <br /> {fullName}
      </h1>

      <div className="bg-[var(--color-dark)] border border-white/20 rounded-lg p-6 w-full max-w-md text-center">
        {book.thumbnail && (
          <img
            src={book.thumbnail}
            alt="Book cover"
            className="w-32 h-auto mx-auto mb-4 rounded"
          />
        )}
        <p>
          <span className="font-semibold">Title:</span> {book.title}
        </p>
        {book.authors && (
          <p>
            <span className="font-semibold">Authors:</span>{" "}
            {book.authors.join(", ")}
          </p>
        )}
        <p>
          <span className="font-semibold">ISBN:</span> {book.isbn}
        </p>
        {book.borrowed_date && (
          <p className="text-sm text-white/60 mt-1">
            Borrowed on {new Date(book.borrowed_date).toLocaleDateString()}
          </p>
        )}

        <button
          onClick={handleReturn}
          className="mt-5 w-full px-4 py-2 rounded-md bg-white/10 hover:bg-white/20 font-medium transition-colors"
        >
          Return Book
        </button>
      </div>
    </div>
  );
}
