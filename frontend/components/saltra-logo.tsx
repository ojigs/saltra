import Link from "next/link";

export function SaltraLogo() {
  return (
    <div className="flex h-full flex-col px-3 py-4 md:px-2">
      <Link
        className="mb-2 flex h-20 items-end justify-start rounded-md bg-blue-600 p-4 md:h-40"
        href="/"
      >
        <div className="w-32 text-white md:w-40">
          <h1 className="text-xl">Saltra</h1>
        </div>
      </Link>
    </div>
  );
}
