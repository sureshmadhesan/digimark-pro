import Layout from "../components/Layout";
import { useState } from "react";
import api from "../services/api";

export default function CampaignWizard() {
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({ ad_account_id: 1, name: "", goal: "TRAFFIC", budget_daily: 500, location: "India", audience: {}, creative: {} as any });
  const [message, setMessage] = useState("");

  const next = () => {
    if (step === 1 && !form.name) return setMessage("Campaign name required.");
    if (step === 2 && form.budget_daily <= 0) return setMessage("Budget must be positive.");
    setMessage("");
    setStep(Math.min(step + 1, 3));
  };

  const submit = async () => {
    try {
      await api.post("/campaigns", form);
      setMessage("Campaign launched successfully.");
    } catch (e: any) {
      setMessage(e?.response?.data?.detail || "Failed to launch campaign.");
    }
  };

  return <Layout>
    <h1 className="text-2xl font-semibold mb-4">Campaign Wizard</h1>
    {step === 1 && <input className="border p-2 w-full" placeholder="Campaign Name" onChange={(e)=>setForm({...form, name: e.target.value})} />}
    {step === 2 && <input className="border p-2 w-full" type="number" placeholder="Daily Budget (INR)" onChange={(e)=>setForm({...form, budget_daily: Number(e.target.value)})} />}
    {step === 3 && <textarea className="border p-2 w-full" placeholder="Creative Headline" onChange={(e)=>setForm({...form, creative: {headline: e.target.value}})} />}
    <div className="mt-4 flex gap-2">
      {step < 3 ? <button className="bg-slate-800 text-white px-4 py-2" onClick={next}>Next</button> : <button className="bg-green-600 text-white px-4 py-2" onClick={submit}>Launch</button>}
    </div>
    {message && <p className="text-sm mt-2">{message}</p>}
  </Layout>;
}
