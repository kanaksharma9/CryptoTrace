import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 text-center">
      <h1 className="text-4xl font-bold tracking-tight text-blue-500 mb-4">
        CryptoTrace
      </h1>
      <p className="text-lg text-slate-400 max-w-xl mb-8">
        Real-Time Crypto Fraud Attribution System
      </p>
      <div className="flex gap-4">
        <Link
          href="/cases"
          className="px-6 py-3 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-medium transition"
        >
          View Cases
        </Link>
        <Link
          href="/login"
          className="px-6 py-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium transition"
        >
          Login
        </Link>
      </div>
    </main>
  );
}
