export default function CaseDetailPage({
  params,
}: {
  params: { id: string };
}) {
  return <main className="p-8">Case {params.id}</main>;
}