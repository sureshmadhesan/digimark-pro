import Layout from "../components/Layout";

export default function Dashboard() {
  return (
    <Layout>
      <h1 className="text-2xl font-semibold mb-4">Dashboard</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          ["Impressions", "120,430"],
          ["Clicks", "8,420"],
          ["Avg CPC", "₹12.3"],
          ["Spend", "₹1,03,600"],
        ].map(([k, v]) => (
          <div key={k} className="bg-white rounded shadow-sm p-4">
            <p className="text-xs text-gray-500">{k}</p>
            <p className="text-xl font-bold">{v}</p>
          </div>
        ))}
      </div>
    </Layout>
  );
}
