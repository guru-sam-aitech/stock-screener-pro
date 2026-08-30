export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-primary-600 mb-4">
          Market Mind
        </h1>
        <p className="text-2xl text-gray-600 mb-8">
          Global Stock Screener & Fundamental Analysis
        </p>
        <p className="text-lg text-gray-500 max-w-2xl">
          Screen stocks across 50+ countries with 5,900+ filters. 
          Combine the best features of Screener.in, Tickertape, TIKR, and Finviz.
        </p>
        <div className="mt-12">
          <button className="bg-primary-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-primary-700 transition">
            Get Started
          </button>
        </div>
      </div>
    </main>
  )
}
