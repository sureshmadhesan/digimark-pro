import Layout from "../components/Layout";
import api from "../services/api";

export default function Billing() {
  const subscribe = async (plan: string) => {
    const { data } = await api.post("/billing/subscriptions", null, { params: { plan_code: plan } });
    alert(`Subscription created: ${data.subscription_id}`);
  };

  return <Layout>
    <h1 className="text-2xl font-semibold mb-4">Billing</h1>
    <div className="grid md:grid-cols-2 gap-4">
      <div className="bg-white p-4 rounded shadow">
        <h2 className="font-semibold">Starter</h2><p>₹2,499/month</p>
        <button className="mt-2 bg-black text-white px-3 py-2" onClick={() => subscribe("plan_starter")}>Subscribe</button>
      </div>
      <div className="bg-white p-4 rounded shadow">
        <h2 className="font-semibold">Growth</h2><p>₹6,999/month</p>
        <button className="mt-2 bg-black text-white px-3 py-2" onClick={() => subscribe("plan_growth")}>Subscribe</button>
      </div>
    </div>
  </Layout>;
}
